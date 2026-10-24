# AB30 O4 — REPAIR R1, disclosed after 30 initial invalid runs and BEFORE repaired replay

The precommitted v1 Python source SHA256 `f800f562eb72d0e5d4784bb8d0ffe35f9f60d5d45e87d49631c4eb452265d47a` wrongly called its deterministic allocation function "Hamilton largest remainders". It repeatedly recomputed remaining shares rather than allocating seats by **fractional remainders of the one-time ideal target**. The actual 30 outcomes B01–B05 were computed, inspected and are now **INVALID_FOR_PREDECLARED_METHOD_IDENTITY**, retained in `results_invalid_v1/` in downloadable archive. The earlier separate pilot on budgets 9/12/16/24/32 is likewise NOT COUNTED.

**Prospective replacement:** replace exactly the source span `def apportion(...)` through just before `def candidates(...)`, leaving all other source bytes fixed, with the following block:
```python
def apportion(target,counts,B):
    """Bounded Hamilton largest remainders after reserving one label per stratum."""
    weights=np.maximum(np.asarray(target,float),0)
    counts=np.asarray(counts,int)
    assert len(weights)==len(counts)==3 and 3<=B<=sum(counts)
    if weights.sum()<=0:weights=np.ones(3)
    weights=weights/weights.sum()
    ideal=1+(B-3)*weights
    v=np.minimum(np.floor(ideal).astype(int),counts)
    v=np.maximum(v,1)
    while v.sum()<B:
        room=np.where(v<counts)[0]
        assert len(room)>0
        i=room[int(np.argmax(ideal[room]-v[room]))]
        v[i]+=1
    while v.sum()>B:
        excess=np.where(v>1)[0]
        i=excess[int(np.argmin(ideal[excess]-v[excess]))]
        v[i]-=1
    assert sum(v)==B and (v>=1).all() and (v<=counts).all()
    return tuple(map(int,v))
```

**Exact SHA256 source after patch:** `ad330115b84f9e47b8d0372c8d3b6222ae5c34b916b0d364d9a34b82c7449b14`, length 8948 bytes, unit test `apportion([.2,.3,.5],[20,30,50],12)==(3,4,5)`. Original source exact parts Git SHA available in this branch.

**Governance:** Source R1 and all v1 numeric outcomes were viewed before this repair. Pre-registering a replay now does NOT produce an independent blind confirmation; all repaired 30 will be transparently tagged `REPAIRED_EXPLORATORY_AFTER_EXPOSURE`. We retain all original source, readouts, and both sets of results with a supersession warning. Never quote initial numerical findings as valid claims about Hamilton or assign 1/3 to them without reevaluation. R5 stopping is overridden by explicit user authorization for exactly 30 valid AB dossiers; invalid 30 remain audit trail not quota.

**R1 pre-execution commitment:** this document + SHA + unit test, committed **before any R1 analysis run**.
