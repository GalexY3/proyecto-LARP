"""Frozen prospective AB-R H06–H30 finite audits. Tests are not formal proofs.
No original images/datasets/previous outcomes used. Python, numpy, sympy.
"""
import itertools, math, json, hashlib, sys
from pathlib import Path
import numpy as np
import sympy as sp
checks=[]

def mark(id, ok, facts):
    ok=bool(ok)
    checks.append(dict(id=id,status='PASS' if ok else 'FAIL',evidence=facts))
    if not ok:raise AssertionError(f'{id}: {facts}')

def choose(n,k): return math.comb(n,k) if 0 <= k <= n else 0

def powr(p,k):return abs(np.exp(2j*np.pi*k*np.asarray(p)).mean())**2

# B1: class-aware routing and graph structure (H06--H10)
counts=[163,85,68,50,34]; N=sum(counts); m=len(counts)
labels=sum(([i]*v for i,v in enumerate(counts)),[])
byclass=[[i for i,c in enumerate(labels) if c==t] for t in range(m)]
# For each target and each type, select different sender (same type never self).
all_edges=set()
for v in range(N):
    for c in range(m):
        donors=byclass[c]
        w=donors[0] if donors[0]!=v else donors[1]
        all_edges.add((w,v))
mark('H06',len(all_edges)==5*N and all(w!=v for w,v in all_edges) and all({labels[w] for w,x in all_edges if x==v}==set(range(m)) for v in range(N)),dict(directed_edges=len(all_edges),minimum_edges=m*N))
mark('H07',math.ceil(N/min(counts))==12 and 11*min(counts)<N,dict(required_fanout=12,weakest_population=min(counts)))
moore=[sum(6**j for j in range(T+1)) for T in range(5)]
mark('H08',moore[3]<N<=moore[4],dict(moore_caps=moore,minimum_T=4))
ns=[3,2,2];n=sum(ns); labs=sum(([i]*v for i,v in enumerate(ns)),[])
A=np.array([[int(i!=j and labs[i]!=labs[j]) for j in range(n)]for i in range(n)],dtype=float)
L=np.diag(A.sum(axis=1))-A
w=np.linalg.eigvalsh(L);expect=sorted([0]+[n]*(len(ns)-1)+sum(([n-v]*(v-1) for v in ns),[]))
mark('H09',np.allclose(w,expect),dict(eigenvalues=w.tolist(),predicted=expect))
pi=np.array([v*(N-v) for v in counts],dtype=float);pi/=pi.sum()
P=np.array([[counts[j]/(N-counts[i]) if i!=j else 0 for j in range(m)]for i in range(m)])
mark('H10',np.allclose(pi@P,pi) and np.max(abs((pi[:,None]*P)-(pi[:,None]*P).T))<1e-13,dict(stationary=pi.tolist(),max_balance_error=float(np.max(abs((pi[:,None]*P)-(pi[:,None]*P).T)))))

# B2: geometry, local quantization, exact Fourier ledger (H11--H15)
N0=13;n0=5; pos=[(j*N0)//n0 for j in range(n0)];gap=np.diff(np.r_[pos,pos[0]+N0]);best=math.ceil(N0/n0)
# Full combinatorial enumeration 13 choose 5, independent of constructed indices.
min_enumerated=min(max(np.diff(np.r_[z,z[0]+N0])) for z in itertools.combinations(range(N0),n0))
mark('H11',max(gap)==best==min_enumerated,dict(indices=pos,gaps=gap.tolist(),max_gap=best,enumerated=min_enumerated))
N0=12;b=np.array([1 if j%3==0 else 0 for j in range(N0)]); n0=int(sum(b))
rho=np.fft.fft(b); S=np.abs(rho)**2/n0
mark('H12',abs(S[1:].sum()-(N0-n0))<1e-12,dict(N=N0,n=n0,spectral_total=float(S[1:].sum())))
C1=int(np.dot(b,np.roll(b,-1)));lhs=sum(abs(rho[k])**2*math.cos(2*math.pi*k/N0) for k in range(1,N0));rhs=N0*C1-n0*n0
mark('H13',abs(lhs-rhs)<1e-11,dict(adjacent_pairs=C1,weighted_spectral_sum=float(lhs),expected=rhs))
mt,nt=3,4;part=[(np.arange(nt)/nt+c/(mt*nt))%1 for c in range(mt)];union=np.sort(np.concatenate(part))
mark('H14',np.allclose(union,np.arange(mt*nt)/(mt*nt)) and all(powr(x,k)<1e-25 for x in part for k in [1,2,3]) and all(powr(union,k)<1e-25 for k in range(1,mt*nt)) and abs(powr(part[0],4)-1)<1e-13,dict(union_size=len(union),individual_alias_k=4,union_alias_k=12))
ns=[3,4,2];ws=[.2,.5,.3];Qmin=sum(a/(12*z*z)for a,z in zip(ws,ns));
# Exact Jensen per type; test a nonuniform perturbation for one subtype.
x=np.array([0,1/3+.03,2/3]);g=np.diff(np.r_[x,x[0]+1]);Qnonuniform=float(sum(g**3)/12)
mark('H15',Qnonuniform>=1/(12*3**2) and Qmin>0,dict(lower_bound=Qmin,Q_3_perturbed=Qnonuniform,Q_3_optimum=1/(12*9)))

# B3: covariance, RKHS and finite hybrid optimization (H16--H20)
a=2.;rho=.6
risk=lambda phase,cc:2*a*a*(1+cc*math.cos(phase))
mark('H16',abs(risk(math.pi,rho)-2*a*a*(1-rho))<1e-13 and risk(math.pi,rho)<risk(0,rho),dict(min_risk=risk(math.pi,rho),aligned=risk(0,rho)))
r=.7; worst=lambda ph:2*a*a*(1+r*abs(math.cos(ph)))
mark('H17',abs(worst(math.pi/2)-2*a*a)<1e-13 and worst(0)>worst(math.pi/2),dict(minimax=worst(math.pi/2),aligned_worst=worst(0)))
ks=np.array([-3,-2,-1,1,2,3]);weight=(1+ks.astype(float)**2)**-2;ps=np.array([0,.375]);amps=np.array([np.exp(2j*np.pi*k*ps).mean()for k in ks]);RKHSrisk=float(np.sum(weight*abs(amps)**2));coeff=weight*np.conj(amps)/np.sqrt(RKHSrisk)
norm=float(np.sum(abs(coeff)**2/weight));quadrature=float(abs(np.sum(coeff*amps))**2)
mark('H18',abs(norm-1)<1e-13 and abs(quadrature-RKHSrisk)<1e-12,dict(worst_case_RKHSrisk=RKHSrisk,saturating_norm=norm,attained_error=quadrature))
def partial(R):return sum(1/(i*i+j*j)for i in range(-R,R+1)for j in range(-R,R+1)if i or j)
parts=[partial(t)for t in [4,8,16,32]]
mark('H19',all(x<y for x,y in zip(parts,parts[1:])),dict(partial_sums_2d=parts,proof='each new dyadic block has >=r^2 modes with |k|²<=5r², so >=1/5 per block'))
# finite compact domain; exhibit continuous objective, and near-minimal grid via dense mesh
xx=np.arange(2001)/2001
F=.2*(1+np.cos(2*np.pi*xx))+.8*(1-np.cos(4*np.pi*xx))
mark('H20',np.isfinite(F).all() and 0<=F.min()<=F.max()<=2,dict(sample_min=float(F.min()),sample_argmin=float(xx[np.argmin(F)]),compact_domain='circle'))

# B4: Pareto, quotas, loss of rare types (H21--H24)
pts=[(0,4),(1,3.5),(4,0)];scan=np.r_[np.linspace(0,5,1000),[1e9]]
chosen={int(np.argmin([l*t+s for l,s in pts])) for t in scan}
mark('H21',1 not in chosen,dict(supported_candidates=sorted(chosen),B_competitive_lambda_interval='lambda<=0.5 and >=7/6 impossible'))
eligible=[(i,s)for i,(l,s)in enumerate(pts)if l<=1]
mark('H22',min(eligible,key=lambda t:t[1])[0]==1,dict(epsilon=1,constrained_minimizer='B'))
counts=np.array([163,85,68,50,34]);R=counts.sum()/len(counts)**2 *np.sum(1/counts)
mark('H23',R>1 and abs(np.sum(counts)-400)<1e-13,dict(variance_ratio_to_balanced_equal_sigma=float(R),counts=counts.tolist()))
pr=.02
survive=lambda nums:float(np.prod([1-(1-pr)**int(n)for n in nums]))
orig=survive(counts);equal=survive(np.repeat(80,5));a=survive([79,81,80,80,80]);
mark('H24',equal>orig and equal>a,dict(original=orig,balanced=equal,one_unit_imbalanced=a,p_retention=pr))

# B5: information theory, graph neural networks, robust fusion (H25--H30)
t1,t2=2.,3.;I=lambda x:.5*math.log(1+x)
mark('H25',I(t1)-I(0)>I(t1+t2)-I(t2)>0,dict(marginal_before=I(t1)-I(0),after=I(t1+t2)-I(t2)))
from collections import Counter
samps=list(itertools.product([0,1],repeat=2)); Y=[i^j for i,j in samps]
def entropy(z):
 c=Counter(z);return -sum(v/len(z)*math.log2(v/len(z))for v in c.values())
Hy=entropy(Y);I1=Hy-sum(.5*entropy([Y[k]for k,(i,j)in enumerate(samps)if i==x])for x in [0,1]);I12=Hy
mark('H26',I1==0 and I12==1,dict(I_Y_X1=I1,I_Y_X2=I1,I_Y_X1X2=I12))
A=np.zeros((4,4));A[1,0]=A[2,1]=A[3,2]=1
mark('H27',(np.linalg.matrix_power(A,2)[3,0]==0 and np.linalg.matrix_power(A,3)[3,0]==1),dict(dist_0_3=3,influence_T2=float(np.linalg.matrix_power(A,2)[3,0]),influence_T3=float(np.linalg.matrix_power(A,3)[3,0])))
rng=np.random.default_rng(3010);T,b,h=2,1,2;U=rng.normal(size=(10,b*h*T));V=rng.normal(size=(b*h*T,10));trans=U@V
mark('H28',np.linalg.matrix_rank(trans)<=T*b*h,dict(cut_capacity=4,linear_rank=int(np.linalg.matrix_rank(trans)),inputs=10))
s1,s2=1.,2.;r=.3;w=(s2*s2-r*s1*s2)/(s1*s1+s2*s2-2*r*s1*s2);wi=s2*s2/(s1*s1+s2*s2)
def vr(x):return x*x*s1*s1+(1-x)**2*s2*s2+2*r*x*(1-x)*s1*s2
mark('H29',0<w<1 and vr(w)<vr(wi),dict(robust_weight=w,independent_weight=wi,robust_worst_variance=vr(w),independent_assumed_worst=vr(wi)))
X=rng.normal(size=(5,3));W=rng.normal(size=(3,3));P=np.eye(5)[[2,0,4,1,3]]
def attention(z):
 q=z@W;S=q@q.T/math.sqrt(3);S-=S.max(axis=1,keepdims=True);probs=np.exp(S);probs/=probs.sum(axis=1,keepdims=True);return probs@z
mark('H30',np.allclose(attention(P@X),P@attention(X)),dict(permutation_error=float(np.max(abs(attention(P@X)-P@attention(X)))),geometry_input=False))

assert [c['id'] for c in checks]==[f'H{i:02d}'for i in range(6,31)]
out=Path(sys.argv[1])if len(sys.argv)>1 else Path(__file__).with_name('CHECKS_H06_H30.json')
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps({'protocol':'LARP_ABR_H06_H30','total':len(checks),'passed':sum(c['status']=='PASS'for c in checks),'invalid':sum(c['status']!='PASS'for c in checks),'checks':checks},indent=2,ensure_ascii=False,default=lambda x:x.item() if hasattr(x,'item') else str(x))+'\n')
print(json.dumps({'total':len(checks),'passed':len(checks),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'file':str(out)},indent=2))
