#!/usr/bin/env python3
"""Rebuild the two O6 CT2 charts, using ONLY numeric checkpoints in CT2_TRAJECTORY.json.
No inferred per-cycle scores. Branch-to-branch jumps are not probabilities.
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BASE=Path(__file__).resolve().parent
j=json.loads((BASE/"CT2_TRAJECTORY.json").read_text(encoding="utf-8"))
data=j["tracks"]
for name,limits in (("CT2_full.png",(0,100)),("CT2_zoom.png",(2,16))):
    fig,ax=plt.subplots(figsize=(13.2,6.4))
    for i,series in enumerate(data):
        pts=series["points"]
        xx=[p["cycle_position"] for p in pts]
        yy=[p["score"] for p in pts]
        ax.plot(xx,yy,marker=["o","s","^","D","v","P","X","h"][i],
                linewidth=1.8,markersize=6,label=series["name"])
        if i>=4:
            ax.annotate(str(yy[-1]), (xx[-1],yy[-1]),xytext=(3,7),textcoords="offset points")
    for pivot in (55,85,105,125,145,160,175):
        ax.axvline(pivot,lw=.8,ls=":",color="gray",alpha=.42)
    ax.set_xlim(-2,195)
    ax.set_ylim(*limits)
    ax.grid(axis="y",alpha=.22)
    ax.set_title("LARP — CT2 por rama; historia y DRIFT de disciplinas D4–D5")
    ax.set_xlabel("Posición acumulativa de expedientes (no fecha ni observaciones independientes)")
    ax.set_ylabel("CT2: juicio ordinal de proximidad a 2/3; NO es probabilidad")
    ax.legend(ncol=2,fontsize=8,loc="upper left" if limits[1]==100 else "upper right")
    fig.tight_layout()
    fig.savefig(BASE/name,dpi=180)
    plt.close(fig)
