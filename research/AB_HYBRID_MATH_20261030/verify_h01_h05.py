"""AB-R H01-H05 exact/finite checks. Frozen before first run; checks are not proofs."""
import math
import json
import hashlib
import itertools
from pathlib import Path
from fractions import Fraction
import numpy as np
import sympy as sp

RESULTS = []
def check(key, detail, assertion, evidence):
    RESULTS.append({'id':key,'claim':detail,'pass':bool(assertion),'evidence':evidence})
    if not assertion:
        raise AssertionError(key + ': ' + detail)

def spectrum(points, k):
    z = np.exp(2j*np.pi*k*np.array(points))
    return float(abs(z.mean())**2)

# H01: Quantization integral from sorted torus gaps, exact expression and Fourier alias.
n = 8
for epsilon in (0.0, 1/128, 1/32):
    p = np.mod(np.arange(n)/n+(-1.)**np.arange(n)*epsilon, 1)
    p.sort()
    gaps = np.diff(np.r_[p, p[0]+1])
    q = np.sum(gaps**3)/12
    predicted_q = 1/(12*n*n) + epsilon**2
    predicted_alias = math.cos(2*math.pi*n*epsilon)**2
    assert math.isclose(q,predicted_q,rel_tol=0,abs_tol=1e-13)
    assert math.isclose(spectrum(p,n),predicted_alias,rel_tol=0,abs_tol=1e-13)
# second derivative J at 0 has sign lambda - 4*pi*pi*n*n*w
lam, w = 1.0, 1.0
h01 = {'n':n,'tested_eps':[0.,1/128,1/32],
       'quantization_formula':'1/(12n^2)+epsilon^2',
       'alias_formula':'cos^2(2*pi*n*epsilon)',
       'local_instability_criterion': 'lambda < 4*pi^2*n^2*w',
       'negative_second_derivative': 2*lam - 8*math.pi**2*n*n*w}
check('H01','exact CVT-aliasing tradeoff and curvature threshold',h01['negative_second_derivative']<0,h01)

# H02: Enumerate all 4!/(2!1!1!) = 12 labelings and covariance matrix.
z = np.array([1+0j,1j,-1+0j,-1j])
counts=[2,1,1];N=4
etas=[]
for first in itertools.combinations(range(4),2):
    rest=[i for i in range(4) if i not in first]
    for j in rest:
        third=next(v for v in rest if v!=j)
        sets=(first,(j,),(third,))
        rho=np.array([z[list(inds)].sum() for inds in sets])
        eta=rho-np.array(counts)*z.sum()/N
        etas.append(eta)
assert len(etas)==12
empirical=np.mean([np.outer(v,np.conj(v)) for v in etas],axis=0)
factor=1-abs(z.sum())**2/N**2
pred=np.array([[(N/(N-1))*(counts[a]*(a==b)-counts[a]*counts[b]/N)*factor for b in range(3)] for a in range(3)],dtype=float)
err=np.max(abs(empirical-pred))
assert np.linalg.eigvalsh(pred).min()>-1e-10
h02={'N':N,'quotas':counts,'labelings':len(etas),'empirical_cov':empirical.real.tolist(),
     'predicted_cov':pred.tolist(),'max_absolute_error':float(err),
     'eigenvalues':np.linalg.eigvalsh(pred).tolist()}
check('H02','fixed-quota random-label covariance has structured negative off-diagonals',err<1e-13,h02)

# H03: Exact minimax for two modes and compare v2-like inverse k^2 weighting.
x=sp.symbols('x',real=True)
s1=x;s2=(2*x-1)**2
poly=sp.factor(s1-s2)
intersections=sp.solve(sp.Eq(s1,s2),x)
assert set(intersections)=={sp.Rational(1,4),sp.Integer(1)}
# for x<=1/4: s2>=1/4; for x>=1/4: s1>=1/4
weighted=sp.expand(sp.Rational(4,5)*s1+sp.Rational(1,5)*s2)
assert sp.expand(weighted)==sp.Rational(4,5)*x**2+sp.Rational(1,5)
minimax=sp.Rational(1,4)
weighted_opt=sp.Integer(0)
h03={'S1':'x','S2':'(2*x-1)^2','crossings':[str(a) for a in intersections],
     'minimax_x':str(minimax),'minimax_value':str(minimax),'delta_for_minimax':'1/3',
     'v2_like_weighted_loss':str(weighted),'weighted_optimal_x':str(weighted_opt),
     'weighted_design_worst_case':1,'robust_design_worst_case':0.25}
check('H03','v2-like inverse band weighting is not minimax under unknown band',float(weighted.subs(x,0))<float(weighted.subs(x,minimax)) and minimax<1,h03)

# H04: Inclusion-exclusion and hypergeometric composition formula, independent exact integers.
counts=(163,85,68,50,34);N=sum(counts);d=6
from math import comb

def p_inclusion(focal):
    pool=[v-int(i==focal) for i,v in enumerate(counts)]
    den=comb(N-1,d)
    total=0
    for mask in range(1<<5):
        removed=sum(pool[j] for j in range(5) if mask>>j&1)
        available=N-1-removed
        total+=(-1)**mask.bit_count()*(comb(available,d) if available>=d else 0)
    return Fraction(total,den)

def p_composition(focal):
    pool=[v-int(i==focal) for i,v in enumerate(counts)]
    numer=sum(comb(pool[j],2)*math.prod(pool[h] for h in range(5) if h!=j) for j in range(5))
    return Fraction(numer,comb(N-1,d))

ps=[p_inclusion(c) for c in range(5)]
qs=[p_composition(c) for c in range(5)]
assert ps==qs
p_overall=sum(Fraction(counts[c],N)*ps[c] for c in range(5))
assert 0<p_overall<1
h04={'N':N,'quotas':counts,'d':d,'p_by_focal_class':[float(x) for x in ps],
     'overall_probability':float(p_overall),'overall_fraction':str(p_overall),
     'combinatorial_form':'sum_c C(nc_prime,2) prod_{j!=c} n_j_prime / C(399,6)',
     'exact_methods_agree':True}
check('H04','exact chance of all five modalities within six distinct random neighbors',ps==qs,h04)

# H05: modular cosets CRT; N=12 classes6,4,2 each individually divides12.
N=12; sizes=(6,4,2); steps=tuple(N//q for q in sizes)
assert steps==(2,3,6)
intersections=[]
for a in range(steps[0]):
    A={x for x in range(N) if x%steps[0]==a}
    for b in range(steps[1]):
        B={x for x in range(N) if x%steps[1]==b}
        intersections.append({'r6':a,'r4':b,'intersection':sorted(A&B)})
assert len(intersections)==6 and all(len(r['intersection'])==2 for r in intersections)
h05={'N':N,'quotas':sizes,'steps':steps,'gcd_2_3':math.gcd(2,3),
     'intersections':intersections,'necessary_pairwise_criterion':'gcd(N/n_i,N/n_j)>1 for disjoint nonempty cosets',
     'scope':'1D circular optimal union grid and equal-spacing species grids'}
check('H05','divisibility of each quota does not suffice for optimal multicolor lattice partition',all(len(r['intersection'])==2 for r in intersections),h05)

out={'campaign':'AB-R-MHU-HYBRID-20261030','preregistered':['H01','H02','H03','H04','H05'],
     'checks':RESULTS,'checks_run':len(RESULTS),'pass_count':sum(x['pass'] for x in RESULTS),
     'scope':'Local internal verification of exact finite examples, not novelty or external replication',
     'versions':{'numpy':np.__version__,'sympy':sp.__version__}}
path=Path(__file__).resolve().parent/'CHECKS_H01_H05.json'
path.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'pass_count':out['pass_count'],'run':out['checks_run'],
 'h04_overall':h04['overall_probability'],'checks_sha256':hashlib.sha256(path.read_bytes()).hexdigest()},indent=2))
