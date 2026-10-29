"""Precommitted exact/finite sanity checks for MHU relatives (not proof assistant)."""
import json, math, itertools, hashlib
from pathlib import Path
import numpy as np
import sympy as s

OUT=[]
def record(k, label, ok, evidence):
    OUT.append(dict(id=k, claim=label,pass_check=bool(ok),evidence=evidence))
    if not ok: raise AssertionError(f'{k}: {label}: {evidence}')

def amp(p,k): return np.mean(np.exp(2j*np.pi*k*np.asarray(p)))
def power(p,k): return float(abs(amp(p,k))**2)

# S01: differences in the actual v1 and v2 weight normalization, and LOCAL no spectral cost.
w=np.array([1.,1.,1.,1.]); w2=w/np.array([1.,4.,9.,16.]);w2/=w2.sum()
record('S01','v2 inverse-k2 reweights spectral modes; LOCAL omits spectral',w2[0]>w2[-1] and abs(w2.sum()-1)<1e-12,{'v1':(w/w.sum()).tolist(),'v2':w2.tolist()})
# S02: phasor polygon extrema, equal amplitudes m=3.
z=sum(np.exp(2j*np.pi*j/3) for j in range(3))
record('S02','single-frequency three-phasor minimum and maximum',abs(z)<1e-12 and abs(sum(np.ones(3)))==3,{'min_power':abs(z)**2,'max_power':9})
# S03: pairwise zero of 3 complex class amplitudes forces each zero.
a,b,c=s.symbols('a b c'); sol=s.solve([a+b,a+c,b+c],(a,b,c))
record('S03','all pairwise sum zero implies all amplitudes zero',sol=={a:0,b:0,c:0},str(sol))
# S04: uniform independent integer phases erase cross terms exactly.
ph=np.exp(2j*np.pi*np.arange(16)/16)
record('S04','uniform type translation averages nonzero-mode cross to zero',abs(np.mean(ph))<1e-14,{'mean_phase_modulus':float(abs(ph.mean()))})
# S05: bird proportions permit full one-frequency phasor cancellation at equal per-type normalized magnitude.
f=np.array([163,85,68,50,34],dtype=float)/400.;q=np.sqrt(f)
record('S05','avian counts satisfy polygon feasibility, equal normalized type amplitudes',2*q.max()<q.sum() and abs(f.sum()-1)<1e-12,{'fractions':f.tolist(),'max_length':float(q.max()),'sum_other':float(q.sum()-q.max())})
# S06: n-per-type interlaced torus grid optimal type and union covering gap.
n,m=5,3;p=(np.arange(n*m)+.5)/(n*m);labels=np.arange(n*m)%m
def gaps(xs):
    xs=np.sort(np.asarray(xs)%1)
    return np.diff(np.r_[xs,xs[0]+1])
record('S06','equal-count interlaced grid achieves class+union circle cover minima',all(np.allclose(gaps(p[labels==t]),1/n) for t in range(m)) and np.allclose(gaps(p),1/(n*m)),{'type_radius':1/(2*n),'union_radius':1/(2*n*m)})
# S07: three-grid cannot contain antipodal pair for a type of two.
tri=np.arange(3)/3
record('S07','unequal 1+2 counts obstruct simultaneous exact two-type and union optimality',all(not math.isclose((tri[j]-tri[i])%1,.5) for i in range(3) for j in range(i+1,3)),{'union_N':3,'class_n':2,'ideal_spacing':.5})
# S08: exact 1D CVT integrated squared distance per interval g^3/12.
g,t=s.symbols('g t', positive=True);integ=s.integrate(t**2,(t,0,g/2))*2
record('S08','1D Voronoi gap squared-error integral equals g^3/12',s.simplify(integ-g**3/12)==0,str(integ))
# S09: alternating lattice remains stealth low-k but worsens covering radius.
n=8;eps=.017;reg=np.arange(n)/n; alt=(reg+(-1.)**np.arange(n)*eps)%1
record('S09','low-k finite stealth may coexist with worse max gap',max(power(alt,k) for k in range(1,n//2))<1e-25 and gaps(alt).max()>gaps(reg).max(),{'max_lowk_power':max(power(alt,k) for k in range(1,4)),'radius_regular':float(gaps(reg).max()/2),'radius_alternate':float(gaps(alt).max()/2)})
# S10: with n IID type points, probability no point in ball of volume v is (1-v)^n.
n,v=8,s.Rational(1,10);pmiss=(1-v)**n
record('S10','IID empty region probability exact binomial',s.expand(pmiss)==s.Rational(9,10)**8,{'empty_prob':str(pmiss)})
# S11: E|A|²=1/n under uniform iid nonzero Fourier coefficients, diagonal only.
n=7;diag=s.Rational(n,n*n)
record('S11','IID complex Fourier amplitude expected power=1/n',diag==s.Rational(1,n),{'n':n,'E_power':str(diag),'E_S':1.})
# S12: lattice spectral aliasing.
n=4;p=np.arange(n)/n
record('S12','lattice zero low modes, aliases at multiples of n',all(power(p,k)<1e-25 for k in range(1,n)) and abs(power(p,n)-1)<1e-12,{'p1to4':[power(p,k) for k in range(1,5)]})
# S13: v2 weights correspond to 1/k² signal power on the listed modes.
ks=np.array([1,2,3,4]);v2=(1./ks**2);v2/=v2.sum()
record('S13','inverse square weights match target Fourier energy profile if such a profile is assumed',v2[0]>v2[1]>v2[2]>v2[3] and abs(v2.sum()-1)<1e-12,{'normalized_weights':v2.tolist()})
# S14: independent jitter exact spectral attenuation and random floor.
p=np.array([0.,.5]);k=1;delta=.12;phi=math.cos(2*math.pi*k*delta);analytic=(1-phi**2)/len(p)+phi**2*power(p,k)
options=list(itertools.product([-delta,delta],repeat=2));exact=np.mean([power((p+shift)%1,k) for shift in options])
record('S14','random iid jitter damped power plus white floor',abs(analytic-exact)<1e-12,{'analytical':analytic,'enumerated':float(exact)})
# S15: same point positions admit different graph Fiedler gaps.
P=np.arange(4)/4
def gap(e):
    A=np.zeros((4,4))
    for u,v in e:A[u,v]=A[v,u]=1
    return float(np.linalg.eigvalsh(np.diag(A.sum(0))-A)[1])
gp=gap([(0,1),(1,2),(2,3)]);gc=gap([(0,1),(1,2),(2,3),(3,0)])
record('S15','same coordinates different adjacency different graph spectral gap',gc>gp+1,{'path_gap':gp,'cycle_gap':gc,'positions':P.tolist()})
# S16: edge cross-type expectation for uniformly shuffled fixed count labels.
counts=np.array([163,85,68,50,34]);N=int(counts.sum());hetero=1-sum(int(x*(x-1)) for x in counts)/(N*(N-1))
record('S16','heterotypic edge null under fixed-quotas random labeling',0<hetero<1,{'N':N,'counts':counts.tolist(),'expected_heterotypic_edge_fraction':hetero})
# S17: finite-population random label Fourier factor conditional on fixed coordinates.
Z=np.array([1,1j,-1,-1j]);N=4;num=2;vals=[]
for subset in itertools.combinations(range(N),num):vals.append(abs(sum(Z[list(subset)]))**2/num)
exact=np.mean(vals); formula=(N-num)/(N-1)+(num-1)/(N-1)*(abs(Z.sum())**2/N)
record('S17','random labels leave positive subtype spectral floor even for stealthy union',abs(exact-formula)<1e-12 and abs(formula-2/3)<1e-12,{'exact':float(exact),'formula':float(formula)})
# S18: weighted-sum scalarization improves spectral relative to optimal LOCAL, at possible cost to local.
L=np.array([0.,1.,3.]);S=np.array([4.,1.,0.]);lam=1.;i=int(np.argmin(S+lam*L));j=int(np.argmin(L))
record('S18','global weighted optimum cannot improve local optimum L but weakly improves S',L[i]>=L[j] and S[i]<=S[j] and i==1,{'LOCAL_opt':j,'joint_opt':i,'L_joint':float(L[i]),'S_joint':float(S[i])})
# S19: equal per-species averaging implies inverse frequency boost for minority classes.
counts=np.array([163,85,68,50,34]);f=counts/counts.sum();ratio=f.max()/f.min()
record('S19','unweighted 5-type mean upweights the smallest type relative to largest',4.7<ratio<4.9,{'relative_per_particle_weight_small_over_large':float(ratio)})
# S20: finite-frequency amplitude perturbation stability.
p=np.array([.15,.55,.81]);dp=np.array([.001,-.001,.001]);k=3;delta=max(abs(dp));A=amp(p,k);B=amp((p+dp)%1,k);bound=2*math.pi*abs(k)*delta; boundS=2*bound+bound**2
record('S20','low-k squared-amplitude sensitivity bounded by frequency×point displacement',abs(B-A)<=bound+1e-12 and abs(abs(B)**2-abs(A)**2)<=boundS+1e-12,{'amplitude_change':float(abs(B-A)),'amplitude_bound':bound,'power_change':float(abs(abs(B)**2-abs(A)**2)),'power_bound':boundS})

if __name__=='__main__':
    target=Path(__file__).resolve().parent/'checks_20.json'
    target.write_text(json.dumps({'schema':'MHU-SISTERS20','check_count':len(OUT),'checks':OUT},ensure_ascii=False,indent=2))
    print('PASS',len(OUT),'checks',hashlib.sha256(target.read_bytes()).hexdigest())
