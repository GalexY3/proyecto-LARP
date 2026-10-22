"""Tables and figures from recorded runs; no inferred or invented results.

This module has no CLI dependency and never updates architecture beliefs.
Failed and incomplete runs remain in the table. Technical and scientific
stages are separated in figures, together with task, variant and score split.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re
from typing import Any

import numpy as np

from .analysis import initial_beliefs
from .artifacts import file_hash, utc_now, write_json


RESULT_COLUMNS = (
    "experiment_id", "stage", "task", "variant", "condition", "geometry_seed",
    "training_seed", "status", "score_split", "score", "loss", "validation_score",
    "validation_loss", "test_score", "test_loss", "updates_completed", "updates_budget",
    "samples_seen", "parameters", "active_edges", "adapter_MAC_per_node",
    "training_seconds_including_periodic_validation", "optimizer_step_seconds_median",
    "optimizer_step_seconds_p90", "RSS_peak_bytes_sampled", "device_peak_bytes",
    "steps_to_validation_threshold", "test_opened", "preregistered",
    "divergence_verified", "infrastructure_excluded", "labels_hash", "code_source_hash",
    "expected_geometry_seeds", "expected_training_seeds", "source_path", "source_sha256",
)
CURVE_COLUMNS = (
    "experiment_id", "stage", "task", "variant", "condition", "geometry_seed",
    "training_seed", "event_index", "time", "update", "optimization_loss",
    "validation_score", "validation_loss", "source_path", "source_sha256",
)


def _number(value: Any) -> float:
    if isinstance(value, dict) and "nonfinite" in value:
        return {"nan": np.nan, "+inf": np.inf, "-inf": -np.inf}.get(value["nonfinite"], np.nan)
    try:
        return float(value) if value is not None else np.nan
    except (TypeError, ValueError):
        return np.nan


def _cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, dict) and "nonfinite" in value:
        return value["nonfinite"]
    if isinstance(value, (list, dict)):
        return json.dumps(value, sort_keys=True, ensure_ascii=False)
    return value


def _csv(path: Path, rows: list[dict[str, Any]], columns: tuple[str, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows({name: _cell(row.get(name)) for name in columns} for row in rows)


def _figure_key(key: tuple[str, ...]) -> str:
    text = "__".join(key)
    readable = re.sub(r"[^A-Za-z0-9_.-]+", "_", text)[:100].strip("_") or "run"
    return readable + "_" + hashlib.sha256(text.encode()).hexdigest()[:8]


def _result_row(record: dict[str, Any], path: Path) -> dict[str, Any]:
    row = {column: record.get(column) for column in RESULT_COLUMNS}
    validation, test = record.get("validation", {}), record.get("test", {})
    if not isinstance(validation, dict):
        validation = {}
    if not isinstance(test, dict):
        test = {}
    row.update(
        validation_score=validation.get("score"), validation_loss=validation.get("loss"),
        test_score=test.get("score"), test_loss=test.get("loss"),
        code_source_hash=record.get("code", {}).get("source_hash"),
        source_path=str(path.resolve()), source_sha256=file_hash(path),
    )
    return row


def _figures(results: list[dict[str, Any]], curves: list[dict[str, Any]], output: Path) -> list[dict[str, Any]]:
    if not results and not curves:
        return []
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt
    figures = []
    by_endpoint: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in results:
        if np.isfinite(_number(row.get("score"))):
            key = tuple(str(row.get(name) or "unspecified") for name in ("task", "stage", "variant", "score_split"))
            by_endpoint[key].append(row)
    for key, rows in sorted(by_endpoint.items()):
        conditions = sorted({str(row.get("condition") or "unspecified") for row in rows})
        fig, ax = plt.subplots(figsize=(max(6, len(conditions) * 1.4), 4.3), layout="constrained")
        for ci, condition in enumerate(conditions):
            selected = [row for row in rows if str(row.get("condition") or "unspecified") == condition]
            offsets = np.linspace(-0.12, 0.12, len(selected)) if len(selected) > 1 else np.zeros(1)
            for offset, row in zip(offsets, selected):
                completed = row.get("status") == "COMPLETE"
                ax.scatter(ci + offset, _number(row["score"]), color="tab:blue" if completed else "tab:red",
                           marker="o" if completed else "x", s=38, alpha=.8)
        ax.set_xticks(range(len(conditions)), conditions, rotation=15)
        ax.set_xlabel("Condición registrada; un punto por corrida")
        ax.set_ylabel("Score registrado")
        ax.set_title(" / ".join(key) + "\nRojo: corrida distinta de COMPLETE")
        ax.grid(axis="y", alpha=.2)
        name = "scores__" + _figure_key(key) + ".png"
        fig.savefig(output / name, dpi=160)
        plt.close(fig)
        figures.append({"path": str((output / name).resolve()), "table": "results.csv",
                        "facet": list(key), "records": len(rows), "inference": "none"})
    by_curve: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in curves:
        key = tuple(str(row.get(name) or "unspecified") for name in ("task", "stage", "variant"))
        by_curve[key].append(row)
    for key, rows in sorted(by_curve.items()):
        runs: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            runs[str(row.get("experiment_id") or row["source_path"])].append(row)
        fig, axes = plt.subplots(1, 2, figsize=(11.3, 4.2), layout="constrained")
        finite_points = 0
        nonfinite_points = 0
        for run_name, points in sorted(runs.items()):
            # Preserve recorded event order, including restarted/repeated updates.
            x = np.array([_number(row.get("update")) for row in points])
            for ax, column in zip(axes, ("validation_score", "optimization_loss")):
                y = np.array([_number(row.get(column)) for row in points])
                usable = np.isfinite(x) & np.isfinite(y)
                finite_points += int(usable.sum())
                nonfinite_points += int((~usable).sum())
                if usable.any():
                    ax.plot(x[usable], y[usable], marker=".", markersize=3, linewidth=1,
                            label=run_name if len(runs) <= 12 else None)
        if not finite_points:
            plt.close(fig)
            continue
        for ax, ylabel in zip(axes, ("Score de validación", "Loss de optimización")):
            ax.set_xlabel("Updates registrados")
            ax.set_ylabel(ylabel)
            ax.grid(alpha=.2)
        if len(runs) <= 12:
            axes[0].legend(fontsize=6, loc="best")
        fig.suptitle(" / ".join(key) + f"; {len(runs)} corridas\nValores no finitos no dibujados: {nonfinite_points}; véase curves.csv")
        name = "curves__" + _figure_key(key) + ".png"
        fig.savefig(output / name, dpi=160)
        plt.close(fig)
        figures.append({"path": str((output / name).resolve()), "table": "curves.csv",
                        "facet": list(key), "runs": len(runs), "events": len(rows),
                        "nonfinite_coordinates_omitted": nonfinite_points, "inference": "none"})
    return figures


def summarize(runroot: str | Path, output: str | Path) -> dict[str, Any]:
    """Write inspectable CSV/JSON/PNG from actual files under ``runroot``.

    Returns a summary manifest. No caller-supplied metric defaults are used.
    Missing/corrupt records become warnings and no pass state is invented.
    Existing AB history is preserved byte-for-byte; a fresh directory receives
    only initial, unchanged priors. This function performs no posterior update.
    """
    runroot, output = Path(runroot).resolve(), Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    paths = sorted(set(runroot.rglob("results.json")) | set(runroot.rglob("*.results.json"))) if runroot.exists() else []
    results, curves, warnings, aggregate_indexes = [], [], [], []
    for path in paths:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(record, list):
                # Suite indexes duplicate per-run result records. Preserve
                # their provenance without counting runs a second time.
                aggregate_indexes.append({"path": str(path.resolve()), "sha256": file_hash(path),
                                          "entries": len(record), "role": "suite_index_only"})
                continue
            if not isinstance(record, dict) or not record.get("experiment_id"):
                raise ValueError("not an experiment result object")
            row = _result_row(record, path)
            results.append(row)
        except (OSError, ValueError, TypeError, AttributeError) as error:
            warnings.append({"path": str(path), "reason": str(error), "status": "INVALID_RECORD"})
            continue
        curve_path = path.parent / "curve.jsonl"
        if not curve_path.exists():
            continue
        try:
            lines = curve_path.read_text(encoding="utf-8").splitlines()
            curve_digest = file_hash(curve_path)
        except OSError as error:
            warnings.append({"path": str(curve_path), "reason": str(error), "status": "UNREADABLE_CURVE"})
            continue
        for event_index, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
                if not isinstance(event, dict) or "update" not in event:
                    raise ValueError("curve event has no update")
                curve = {name: row.get(name) for name in CURVE_COLUMNS}
                curve.update({name: event.get(name) for name in
                              ("time", "update", "optimization_loss", "validation_score", "validation_loss")})
                curve.update(event_index=event_index, source_path=str(curve_path.resolve()), source_sha256=curve_digest)
                curves.append(curve)
            except (ValueError, TypeError) as error:
                warnings.append({"path": str(curve_path), "line": event_index,
                                 "reason": str(error), "status": "INVALID_CURVE_EVENT"})
    _csv(output / "results.csv", results, RESULT_COLUMNS)
    _csv(output / "curves.csv", curves, CURVE_COLUMNS)
    write_json(output / "results_table.json", results)
    write_json(output / "curves_table.json", curves)
    figure_manifest = _figures(results, curves, output)
    history_path = output / "AB_history.json"
    if not history_path.exists():
        write_json(history_path, {
            **initial_beliefs(), "created_UTC": utc_now(), "created_by": "reporting.summarize",
            "updates": [], "reporting_changes_architecture_beliefs": False,
        })
    summary = {
        "created_UTC": utc_now(), "run_root": str(runroot), "output": str(output),
        "result_files_found": len(paths), "result_records_loaded": len(results),
        "curve_events_loaded": len(curves), "status_counts": dict(Counter(str(row.get("status") or "UNSPECIFIED") for row in results)),
        "stage_counts": dict(Counter(str(row.get("stage") or "UNSPECIFIED") for row in results)),
        "figures": figure_manifest, "warnings": warnings,
        "source_results": [{"path": row["source_path"], "sha256": row["source_sha256"]} for row in results],
        "aggregate_indexes": aggregate_indexes,
        "AB_history": str(history_path), "AB_history_sha256": file_hash(history_path),
        "architecture_beliefs_updated_by_reporting": False,
        "note": "Descriptive tables and figures from recorded files; failures retained, no architecture conclusion.",
    }
    write_json(output / "summary.json", summary)
    return summary
