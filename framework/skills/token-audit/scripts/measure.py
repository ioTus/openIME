#!/usr/bin/env python3
"""Token audit measurement. Reads files from disk — never into model context.

Usage:
    python3 measure.py <repo-root>                 # all files by cost
    python3 measure.py <repo-root> --sections FILE # section breakdown
    python3 measure.py <repo-root> --dupes         # duplication report
    python3 measure.py <repo-root> --hot F1 F2 ... # hot-path total

No public Claude tokenizer exists. chars/3.7 approximates English
technical markdown within about +/-8%. For exact counts use the
Anthropic count_tokens API endpoint.
"""
import os, re, sys, difflib, hashlib
from collections import defaultdict

MID = 3.7
def est(chars): return chars / MID

SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", "dist", "build"}

def walk(root):
    for dp, dn, fns in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for fn in fns:
            yield os.path.join(dp, fn)

def read(p):
    try:
        return open(p, encoding="utf-8").read()
    except (UnicodeDecodeError, OSError):
        return None

def scan(root):
    rows = []
    for p in walk(root):
        t = read(p)
        if t is None:
            continue
        rows.append({"path": os.path.relpath(p, root), "chars": len(t),
                     "lines": t.count("\n") + 1, "tok": round(est(len(t)))})
    return sorted(rows, key=lambda r: -r["chars"])

def cmd_all(root):
    rows = scan(root)
    total = sum(r["chars"] for r in rows)
    print(f"{len(rows)} text files, ~{round(est(total)):,} tok total\n")
    print(f"{'tokens':>8}  {'lines':>6}  path")
    print("-" * 74)
    for r in rows[:40]:
        print(f"{r['tok']:>8,}  {r['lines']:>6,}  {r['path']}")

def cmd_sections(root, rel):
    t = read(os.path.join(root, rel))
    if t is None:
        sys.exit(f"cannot read {rel}")
    parts = re.split(r"^(## .*)$", t, flags=re.M)
    secs = []
    if parts[0].strip():
        secs.append(("(preamble)", len(parts[0])))
    for i in range(1, len(parts), 2):
        body = parts[i + 1] if i + 1 < len(parts) else ""
        secs.append((parts[i].strip(), len(parts[i]) + len(body)))
    total = sum(c for _, c in secs) or 1
    print(f"{rel} — ~{round(est(len(t))):,} tok\n")
    for head, chars in sorted(secs, key=lambda s: -s[1]):
        print(f"  {round(est(chars)):>6,} tok  {100*chars/total:>5.1f}%  {head[:56]}")

def paragraphs(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    out = []
    for b in re.split(r"\n\s*\n", text):
        b = b.strip()
        if not b or b.startswith(("#", "|", "---")) or re.match(r"^[-*>]|\s*\d+\.", b):
            continue
        out.append(" ".join(b.split()))
    return out

def cmd_dupes(root, exts=(".md",)):
    # byte-identical files
    h = defaultdict(list)
    for p in walk(root):
        try:
            h[hashlib.sha256(open(p, "rb").read()).hexdigest()].append(
                (os.path.relpath(p, root), os.path.getsize(p)))
        except OSError:
            continue
    ident = [v for v in h.values() if len(v) > 1]
    print("=== BYTE-IDENTICAL FILES ===")
    if not ident:
        print("  none")
    waste = 0
    for v in sorted(ident, key=lambda v: -v[0][1]):
        waste += v[0][1]
        print(f"  ~{round(est(v[0][1])):,} tok each:")
        for rel, _ in sorted(v):
            print(f"      {rel}")
    if ident:
        print(f"  -> ~{round(est(waste)):,} tok redundant")

    # near-duplicate prose across files
    allp = []
    for p in walk(root):
        if not p.endswith(exts):
            continue
        t = read(p)
        if t is None:
            continue
        for para in paragraphs(t):
            if len(para) > 80:
                allp.append((os.path.relpath(p, root), para))
    print("\n=== NEAR-DUPLICATE PROSE ACROSS FILES ===")
    seen, found = set(), 0
    for i in range(len(allp)):
        for j in range(i + 1, len(allp)):
            if allp[i][0] == allp[j][0]:
                continue
            r = difflib.SequenceMatcher(None, allp[i][1].lower(),
                                        allp[j][1].lower()).ratio()
            if r > 0.55:
                key = tuple(sorted([allp[i][1][:50], allp[j][1][:50]]))
                if key in seen:
                    continue
                seen.add(key)
                found += 1
                if found <= 10:
                    print(f"\n  {r:.0%} similar (~{round(est(min(len(allp[i][1]), len(allp[j][1])))):,} tok)")
                    print(f"    {allp[i][0]}")
                    print(f"    {allp[j][0]}")
                    print(f"    \"{allp[i][1][:84]}...\"")
    print(f"\n  {found} near-duplicate pair(s)")

def cmd_hot(root, rels):
    total = 0
    print("=== HOT PATH (loaded every session) ===")
    for rel in rels:
        t = read(os.path.join(root, rel))
        if t is None:
            print(f"  {'MISSING':>9}  {rel}")
            continue
        total += len(t)
        print(f"  ~{round(est(len(t))):>7,} tok  {rel}")
    print("-" * 46)
    print(f"  ~{round(est(total)):>7,} tok  TOTAL PER SESSION")
    print(f"\n  over a 20-turn session: ~{round(est(total))*20:,} tok processed")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = sys.argv[1]
    if not os.path.isdir(root):
        sys.exit(f"not a directory: {root}")
    args = sys.argv[2:]
    if not args:
        cmd_all(root)
    elif args[0] == "--sections":
        cmd_sections(root, args[1])
    elif args[0] == "--dupes":
        cmd_dupes(root)
    elif args[0] == "--hot":
        cmd_hot(root, args[1:])
    else:
        sys.exit(__doc__)
