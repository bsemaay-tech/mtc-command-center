"""Lead mechanical check of the corrected P012 packet: every `path:line` citation is opened in the REAL source file;
when the packet quotes the line ("..." after the em dash) the quote must be a whitespace-normalized substring of it.
Read-only; writes only its report next to itself."""
import re, pathlib, collections, json, hashlib

PACKET = pathlib.Path("C:/tmp/P012_RISK_20260914/P012_PRODUCTION_ADMISSION_PACKET.md")
OUT = pathlib.Path(__file__).with_name("LEAD_CITATION_CHECK.md")
text = PACKET.read_text(encoding="utf-8")
lines = text.split("\n")
norm = lambda s: re.sub(r"\s+", " ", s).strip()
cache = {}
def src_lines(p):
    if p not in cache:
        fp = pathlib.Path(p)
        cache[p] = fp.read_text(encoding="utf-8").split("\n") if fp.exists() else None
    return cache[p]

pat = re.compile(r"`([A-Za-z]:/[^`]+?):(\d+)`(?:\s*[—-]+\s*[\"“](.*?)[\"”](?=\s*(?:$|\||;|,|\.|\)|—|-)))?")
rows = []; stats = collections.Counter()
for i, ln in enumerate(lines, 1):
    for m in pat.finditer(ln):
        p, n, q = m.group(1), int(m.group(2)), m.group(3)
        sl = src_lines(p)
        if sl is None:
            status = "FILE_MISSING"
        elif n < 1 or n > len(sl):
            status = f"LINE_OUT_OF_RANGE(file has {len(sl)} lines)"
        elif q is None:
            status = "LINE_EXISTS(no quote to compare)"
        else:
            src = norm(sl[n - 1]); qq = norm(q)
            if qq and qq in src:
                status = "EQUAL"
            else:
                # search the whole file for the quote to report the actual line
                hits = [k + 1 for k, s in enumerate(sl) if qq and qq in norm(s)]
                status = f"WRONG_LINE(found at {hits})" if hits else "QUOTE_NOT_FOUND"
        stats[status.split("(")[0]] += 1
        rows.append((i, p.split("/")[-1], n, status, (q or "")[:90]))

sha = hashlib.sha256(PACKET.read_bytes()).hexdigest()
out = [f"# LEAD_CITATION_CHECK — corrected P012 packet (sha256 {sha}), mechanical, read-only", "",
       f"Citations found: {len(rows)}; distinct path:line: {len({(r[1], r[2]) for r in rows})}", "",
       "Status counts: " + ", ".join(f"{k}={v}" for k, v in sorted(stats.items())), "",
       "## Non-EQUAL rows (packet line | source file | cited line | status | quote head)"]
for r in rows:
    if r[3] != "EQUAL":
        out.append(f"- {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]}")
out += ["", "## All rows", ""] + [f"- {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]}" for r in rows]
OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"citations={len(rows)}", dict(stats))
for r in rows:
    if r[3] != "EQUAL":
        print(r)
