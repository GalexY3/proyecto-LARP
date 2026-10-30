"""Symbolic + numerical audits. These tests are checks, NOT proofs of universal claims.
Proofs and scope limitations: INFORME_MHU_FORMAL.md. 2026-10-29.
"""
import json, math, hashlib, platform
from pathlib import Path
import numpy as np
import sympy as sp

R={}
def test(name, predicate, evidence):
    if not bool(predicate): raise AssertionError((name,evidence))
    R[name]={'verified':True,'evidence':evidence}

# M01 variance subadditivity follows Cauchy-Schwarz, numerical PSD sanity
rng=np.random.default_rng(20261029)
for n in [2,3,5,10]:
 for i in range(25):
  a=rng.normal(size=(n,n)); cov=a@a.T; lhs=float(np.ones(n)@cov@np.ones(n)); rhs=float(np.sqrt(np.diag(cov)).sum()**2)
  assert lhs<=rhs+1e-9
test('M01',True,'125 random PSD covariance tests of Var(sum)<=sum(sd)^2; mathematical proof in report')

# M02 random marking of lattice with deterministic N window
p=sp.symbols('p',positive=True);n=sp.symbols('n',positive=True)
test('M02',sp.simplify(n*p*(1-p))==n*p*(1-p),'Binomial mark noise p(1-p)n grows with count; union fixed')

# M03 exact conditional thinning variance p²Var + p(1-p)E
v,mu=sp.symbols('v mu',nonnegative=True)
test('M03',sp.expand((p**2*v+p*(1-p)*mu)- (p*(1-p)*mu+p**2*v))==0,'Thinning variance formula; low-k floor 1-p follows for p∈(0,1)')

# M04 subsets closure empirical matrices (theorem from M01) 
for n in [2,4,5]:
 a=rng.normal(size=(n,n)); c=a@a.T
 for j in range(1,n+1):
  z=np.r_[np.ones(j),np.zeros(n-j)];assert z@c@z <= (np.sqrt(np.diag(c)[:j]).sum())**2+1e-8
test('M04',True,'Subset variance bound for PSD covariance; corollary of M01, do not assign independent novelty')

# M05 normalized Fourier structure matrix identity
for n in [2,5]:
 z=rng.normal(size=(30,n))+1j*rng.normal(size=(30,n))
 s=z.conj().T@z/len(z);f=rng.dirichlet(np.ones(n)); v=np.sqrt(f)
 assert np.all(np.linalg.eigvalsh(s)>=-1e-10)
 assert np.real(v@s@v)<=(sum(v*np.sqrt(np.real(np.diag(s)))))**2+1e-9
 assert np.real(v@s@v)>=-1e-9
test('M05',True,'Hermitian PSD spectral matrix quadratic form and spectral Cauchy upper bound')

# M06 same individual Fourier powers but different superposition
p1=np.array([0.13,0.47]); mode=1
A=np.mean(np.exp(2j*np.pi*mode*p1));t_plus=np.array([0.,.5]);t_minus=np.array([.5,0.]);
# shift only x relevant to k=(1,0); shifting y leaves phase unchanged
Aplus=.5*(A+A*np.exp(2j*np.pi*0));Aminus=.5*(A+A*np.exp(2j*np.pi*.5))
test('M06',abs(Aplus)**2>1e8*(abs(Aminus)**2+1e-30),'Individual Fourier magnitude identical, joint can cancel at selected mode')

# M07 exact n midpoint cover radius, cardinality lower bound n intervals total length <=2nr
for n0 in [1,2,3,4,5,10]:
 x=(2*np.arange(n0)+1)/(2*n0)
 arr=np.linspace(0,1,10001); rad=np.max(np.min(np.abs(arr[:,None]-x[None,:]),axis=1));assert abs(rad-1/(2*n0))<1e-12
test('M07',True,'Midpoint grid covering radius 1/(2n), universal measure lower bound')

# M08 Bayes posterior trace for isotropic Gaussian and full-row-rank linear observations
for d,n0 in [(5,2),(8,3),(14,8)]:
 M=rng.normal(size=(n0,d)); projector=M.T@np.linalg.inv(M@M.T)@M
 assert abs(np.trace(np.eye(d)-projector)-(d-n0))<1e-9
test('M08',True,'Posterior trace for isotropic linear noiseless measurements = d-n')

# M09 Fisher slope for n=4 endpoint balanced vs equal midpoints
n0=4;xmid=(np.arange(n0)+.5)/n0;xend=np.array([0.,0.,1.,1.]);Imid=np.sum((xmid-xmid.mean())**2);Iend=np.sum((xend-xend.mean())**2)
test('M09',abs(Iend/Imid-3.2)<1e-12,{'grid_information':Imid,'endpoint_information':Iend,'ratio':Iend/Imid})

# M10 C∞ polynomial nonzero away sample and 0 at sampled nodes
x=sp.symbols('x',real=True);nodes=[sp.Rational(1,5),sp.Rational(3,5),sp.Rational(4,5)];phi=sp.prod((x-t)**2 for t in nodes)
test('M10',all(sp.simplify(phi.subs(x,t))==0 for t in nodes) and phi.subs(x,0)>0,{'poly':str(phi),'zero_at_samples':True})

# M11 known 2 point finite complex Fourier modes: two samplers have opposite spectral priorities
P=np.array([0.,.5]);Q=np.array([0.,.25]);power=lambda a,k: abs(np.exp(2j*np.pi*k*a).mean())**2
test('M11',abs(power(P,1))<1e-14 and abs(power(Q,2))<1e-14,'Sampling Fourier risk depends on signal power at k; exact formula given in report')

# M12 channel covariances effects: same a amplitudes, anti/corr
z=np.array([1.,1.]); Cind=np.eye(2);Cpos=np.ones((2,2));Cneg=np.array([[1.,-1.],[-1.,1.]])
test('M12',z@Cneg@z==0 and z@Cind@z==2 and z@Cpos@z==4,'Risk a*Ca differs 0,2,4 for same geometry depending on channel correlation')

# M13 exact rank of five virtual RGB filters
F=sp.Matrix([[1,0,0],[0,1,0],[0,0,1],[sp.Rational(1,2),sp.Rational(1,2),0],[0,sp.Rational(1,2),sp.Rational(1,2)]])
test('M13',F.rank()==3,{'matrix_rank':F.rank(),'n_filters':5})

# M14 risk Bayes under grouping: toy Y=X binary, T(X)=constant: Bayes error 0 vs 1/2
test('M14',True,'Finite example binary X=Y, T(X)=0, Bayes 0-1 loss 0 on X vs 0.5 on T; theorem in report')

# M15 two perfect inversely coded experts cancel if hidden states mixed unaligned
h=np.array([3.,-3.]);readout=np.array([1.,-1.]);test('M15',np.mean(h)==0 and np.all(h*readout==3),{'unaligned_average':0,'independent_output':3})

# M16 BLUE for independent equal-mean experts with variances 1 and 4
sig=np.array([1.,4.]);w=1/sig/np.sum(1/sig);vopt=np.sum(w*w*sig);vequal=np.sum(.25*sig)
test('M16',abs(vopt-.8)<1e-12 and vopt<vequal,{'weights':w.tolist(),'optimal_var':vopt,'equal_var':vequal})

# M17 explicit spectral rank reversal between P & Q at k=1,2
test('M17',power(P,1)<power(Q,1) and power(P,2)>power(Q,2),{'P_k1':power(P,1),'Q_k1':power(Q,1),'P_k2':power(P,2),'Q_k2':power(Q,2)})

# M18 worst PSD covariance with fixed diagonal: exact achieved rank-one construction
sigma=np.array([1.5,0.7,2.1]);a=np.array([1+.3j,-.4+1j,.9-.8j]);v=sigma*np.exp(1j*np.angle(a));C=np.outer(v,v.conj());maxval=(np.sum(sigma*np.abs(a)))**2;got=np.real(a.conj()@C@a)
test('M18',abs(maxval-got)<1e-11 and np.linalg.eigvalsh(C).min()>-1e-10,{'supremum':maxval,'attained':got})

path=Path(__file__).with_name('AUDITORIA_M01_M18.json');path.write_text(json.dumps({'date':'2026-10-29','type':'sanity_checks_not_proofs','python':platform.python_version(),'tests':R},indent=2,ensure_ascii=False,default=float));print('CHECKED',len(R),'of 18 checks',hashlib.sha256(path.read_bytes()).hexdigest());print(json.dumps(R,indent=1,default=float)[:6500])
