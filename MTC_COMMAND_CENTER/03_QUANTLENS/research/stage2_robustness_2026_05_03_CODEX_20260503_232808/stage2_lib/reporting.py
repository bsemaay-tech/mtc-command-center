from __future__ import annotations


def md_table(rows: list[dict], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    out = ["|" + "|".join(fields) + "|", "|" + "|".join(["---"] * len(fields)) + "|"]
    for row in rows:
        out.append("|" + "|".join(str(row.get(field, "")).replace("|", "/") for field in fields) + "|")
    return "\n".join(out)
