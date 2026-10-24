#!/usr/bin/env python3
"""Regenerate the two AB O6 CT2 plots from the versioned campaign trajectory."""
from pathlib import Path
import json
import matplotlib.pyplot as plt

base=Path(__file__).resolve().parent
p=json.loads((base/"CT2_TRAJECTORY.json").read_text(encoding="utf-8"))
timeline=p["points"]
xs=[r["sequence"] for r in timeline]
ys=[r["ct2"] for r in timeline]
alt=p["alternate_branch"]["point"]
for zoom in [False,True]:
    fig,ax=plt.subplots(figsize=(11,4.5))
    ax.plot(xs,ys,marker="o",linewidth=2,label=p["main_branch"])
    ax.scatter([alt["sequence"]],[alt["ct2"]],marker="D",s=80,label="D3.7: solo planificación")
    ax.axvspan(20,25,alpha=.09,label="Cinco planes AB")
    ax.axvline(25,ls="--",alpha=.5)
    ax.annotate("CT2 final: 8/100",(55,8),xytext=(-110,22),
                textcoords="offset points",arrowprops={"arrowstyle":"->"})
    ax.set_xlim(0,57)
    ax.set_ylim(6,14.5) if zoom else ax.set_ylim(0,100)
    ax.set_xlabel("Índice de autorización: 20 auditorías + 5 planes + 30 auditorías")
    ax.set_ylabel("CT2 (ordinal 1–100; no es una probabilidad)")
    ax.set_title("LARP AB55 — confianza CT2"+(" (vista ampliada)" if zoom else " (escala completa)"))
    ax.grid(alpha=.2)
    ax.legend()
    fig.tight_layout()
    dst=base/("CT2_ZOOM.png" if zoom else "CT2_100.png")
    fig.savefig(dst,dpi=180)
    plt.close(fig)
    print(dst)
