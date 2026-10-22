"""Separate transportability check, NOT an additional formal AB cycle.
Physical observations: NOAA ERSST.V3B Nino 1+2 SST, statsmodels elnino.
Single 1D series, no multiple channel types; NOT a validation of COSI multichannel.
"""
import itertools,json,numpy as np
from pathlib import Path
from statsmodels.datasets import elnino
P=Path(__file__).resolve().parent
x=elnino.load_pandas().data
v=x.drop(columns='YEAR').to_numpy()
tr=v[:27];val=v[27:46];te=v[46:]
J=list(itertools.combinations(range(12),4))
def calc(z,subset):return float(np.sqrt(np.mean((z[:,list(subset)].mean(axis=1)-z.mean(axis=1))**2)))
def risk_cov(train,shrink):
 z=train-train.mean(axis=1,keepdims=True)
 C=z.T@z/len(z)
 # Intra-year smooth stationarity circulant covariance from average along time diagonals.
 circ=np.zeros((12,12))
 for a in range(12):
  for b in range(12):
   offset=(b-a)%12
   circ[a,b]=np.mean([C[u,(u+offset)%12] for u in range(12)])
 cc=(1-shrink)*circ+shrink*C
 scores=[]
 for t in J:
  h=np.zeros(12);h[list(t)]=.25
  scores.append(float(h@cc@h))
 return J[int(np.argmin(scores))]
def train_opt(train):return min(J,key=lambda j:calc(train,j))
uniform=(0,3,6,9);diag=[]
for n in [6,12,20,27]:
 train=tr[:n]
 for algorithm in ['QUARTERLY','TRAIN_DIRECT','CIRCULANT_REGULARIZED','COV_EMPIRICAL','COV_HALF']:
  if algorithm=='QUARTERLY':chosen=uniform
  elif algorithm=='TRAIN_DIRECT':chosen=train_opt(train)
  elif algorithm=='CIRCULANT_REGULARIZED':chosen=risk_cov(train,0)
  elif algorithm=='COV_EMPIRICAL':chosen=risk_cov(train,1)
  else:chosen=risk_cov(train,.5)
  diag.append({'n_pilot_years':n,'method':algorithm,'months_1_based':[x+1 for x in chosen],
               'development_rmse_c':calc(val,chosen),'heldout_rmse_c':calc(te,chosen)})
report={'status':'ADDITIONAL_TRANSPORTABILITY_PIVOT_NOT_31ST_CYCLE','source':'statsmodels elnino NOAA ERSST.V3B Nino 1+2 SST','years':list(map(int,x.YEAR.to_numpy())),'split':{'train':'1950–1976','development':'1977–1995','test':'1996–2010'},'sensor_budget':'4 monthly temperature measurements/year to estimate annual mean','results':diag,
'limits':['One multiyear site/region only; temporal (1D), not 3D or multichannel','Heldout 1996–2010 was evaluated for all choices and treated as explorative comparisons not repeated independent tests','Scoring monthly average temperature not forecasting or uncertainty calibration']}
(P/'temporal_pivot.json').write_text(json.dumps(report,indent=2))
print('n=12',[(z['method'],z['months_1_based'],round(z['heldout_rmse_c'],3)) for z in diag if z['n_pilot_years']==12])
print('n=27',[(z['method'],z['months_1_based'],round(z['heldout_rmse_c'],3)) for z in diag if z['n_pilot_years']==27])
