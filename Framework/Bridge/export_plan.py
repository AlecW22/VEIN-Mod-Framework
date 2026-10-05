import json
from pathlib import Path


def build_load_plan(resolution_result):
    return {
        "frameworkVersion": "0.2",
        "loadOrder": list(resolution_result.load_order),
        "disabled": dict(resolution_result.disabled),
        "errors": list(resolution_result.errors),
    }


def export_load_plan(
    resolution_result,
    output_path="build/vein_load_plan.json",
):
    output = Path(output_path)

    output.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    plan = build_load_plan(
        resolution_result
    )

    with output.open(
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            plan,
            file,
            indent=2,
            sort_keys=True
        )

    return output