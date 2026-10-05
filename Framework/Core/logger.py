def build_report(scan_result, resolution_result):
    lines = [
        "[VEIN Mod Framework]",
        "Framework Core v0.1",
        "",
        "Scanning Mods...",
        "",
        f"Found {len(scan_result.mods)} valid manifest(s)",
        "",
    ]

    for error in scan_result.errors:
        lines.append(f"[ERROR] {error}")

    if scan_result.errors:
        lines.append("")

    for mod_id in sorted(scan_result.mods):
        if mod_id in resolution_result.disabled:
            lines.append(f"[DISABLED] {mod_id}")
            lines.append(
                f"Reason: "
                f"{resolution_result.disabled[mod_id]}"
            )
        else:
            lines.append(f"[OK] {mod_id}")

    if resolution_result.errors:
        lines.append("")

        for error in resolution_result.errors:
            lines.append(f"[ERROR] {error}")

    lines.extend([
        "",
        "Resolved load order:",
    ])

    if not resolution_result.load_order:
        lines.append("No mods scheduled to load.")
    else:
        for index, mod_id in enumerate(
            resolution_result.load_order,
            start=1
        ):
            lines.append(f"{index}. {mod_id}")

    return "\n".join(lines)