"""Post-selection ablation; NOT counted among 30 preregistered AB cycles."""
import json,sys
from pathlib import Path
import numpy as np
from safety import observations,EXPERTS,methods
from legacy_engine import forecast,split

def compute(name):
    full=observations(name); sp=split(len(full)); end=sp["validation"][1]
    y=full[:end]; base,_=forecast(y,sp["development"])
    full_predictions,_=methods(y,sp["development"])
    diagonal=np.full(len(y),np.nan)
    for t in range(max(40,sp["development"][0]),len(y)):
        positions=np.arange(max(20,t-24),t)
        errors=np.column_stack([y[positions]-base[k][positions] for k in EXPERTS])
        gram=errors.T@errors/len(positions)
        ridge=max(float(np.trace(gram))/3,1e-8)
        weights=1/(np.diag(gram)+ridge)
        weights/=weights.sum()
        diagonal[t]=weights@np.array([base[k][t] for k in EXPERTS])
    start,stop=sp["validation"]
    d=np.abs(y[start:stop]-full_predictions["shrink"][start:stop])-np.abs(y[start:stop]-diagonal[start:stop])
    return {"dataset":name,"delta_full_minus_diagonal":float(d.mean()),"n":len(d),"semantics":"post-test-selected exploratory mechanism ablation","data_source":"historical statsmodels"}
if __name__=="__main__":
    records=[compute(n) for n in ("nile","sunspots","co2","elnino","unemployment","inflation")]
    Path(sys.argv[1]).write_text(json.dumps(records,indent=2)+"\n")
    print(json.dumps(records,indent=2))
