"""Scientific constants loaded unchanged from the authoritative review JSON."""
from pathlib import Path
import json
import numpy as np
from .artifacts import digest, file_hash

ROOT = Path(__file__).resolve().parents[2]


def contract():
    return load_profile("scientific_contract")["larp_v0_1_decisions"]


def load_profile(name):
    path = ROOT / "configs" / (name + ".json")
    value = json.loads(path.read_text(encoding="utf-8"))
    index_path = ROOT / "configs" / "preset_hashes.json"
    if index_path.exists():
        expected = json.loads(index_path.read_text(encoding="utf-8"))[path.name]
        if file_hash(path) != expected:
            raise ValueError("Immutable preset changed: freeze a new protocol version first")
    return value


TASK_KEYS = {"xor": 1, "copy": 2, "fill": 3, "resource": 4}
STAGE_KEYS = {"pilot": 10, "screen": 10, "confirmation": 20, "calibration": 30, "smoke": 40, "integration": 50}
SPLIT_KEYS = {"train": 5001, "validation": 5002, "test": 5003}


def dataset_seed(task, stage, split):
    return int(np.random.SeedSequence([20261008, TASK_KEYS[task], STAGE_KEYS[stage], SPLIT_KEYS[split]]).generate_state(1)[0])


def optimizer_settings(lr=0.003):
    return {"name": "AdamW", "lr": float(lr), "betas": [0.9, 0.999], "eps": 1e-8,
            "weight_decay": 1e-4, "gradient_clip": 1.0, "lr_schedule": "constant",
            "parameter_groups": "all_trainable"}
