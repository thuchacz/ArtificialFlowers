#!/usr/bin/env python3
"""Mechanical pre-audit + taxonomy review table for artificial_flowers.xml.

Outputs (markdown):
  TAXONOMY_REVIEW.md      - per-category usage table for editor sign-off
  PREAUDIT_CANDIDATES.md  - untagged occurrences of known category spellings,
                            classified retroactive vs possible-miss, plus
                            structural checks (union rule, layer parity).
Decides nothing; produces candidates for the second-pass audit.
"""
import re, subprocess, sys, unicodedata
from collections import defaultdict

REPO = "/Users/thc4/Github/ArtificialFlowers"
XML = f"{REPO}/artificial_flowers.xml"

# boundary commits, oldest first: (commit, chunk-number-by-end-of-commit, label)
BOUNDARIES = [
    ("a17acc6", 0, "seed"),
    ("a543bdb", 3, "1-3"),
    ("347549a", 4, "4"),
    ("5fc0145", 5, "5"),
    ("233a5ee", 6, "6"),
    ("eb7594d", 7, "7"),
    ("e1c3c47", 8, "8"),
]

# folio -> chunk number
def folio_chunk(f):
    n = int(f[1:])
    if n <= 3: return 0
    if n <= 16: return 1
    if n <= 29: return 2
    if n <= 42: return 3
    if n <= 57: return 4
    if n <= 69: return 5
    if n <= 123: return 6
    if n <= 143: return 7
    return 8

def norm(s):
    s = s.lower().replace("ū", "u")  # ū -> u  (1:1, keeps offsets)
    return s

text = open(XML, encoding="utf-8").read()

# --- categories -------------------------------------------------------------
cats = {}          # id -> (label, group)
group = None
for m in re.finditer(r'<taxonomy xml:id="(\w+)">|<bibl>([^<]+)</bibl>|<category xml:id="(\w+)"><catDesc>([^<]+)</catDesc>', text):
    if m.group(1): group = m.group(1)
    elif m.group(3): cats[m.group(3)] = (m.group(4), group)

# minting chunk per category id
minted = {}
for commit, num, label in BOUNDARIES:
    try:
        old = subprocess.run(["git", "-C", REPO, "show", f"{commit}:artificial_flowers.xml"],
                             capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        continue
    for cid in re.findall(r'<category xml:id="(\w+)"', old):
        if cid not in minted:
            minted[cid] = (num, label)
for cid in cats:
    minted.setdefault(cid, (8, "8"))

# --- layer + folio maps ------------------------------------------------------
tc_start = text.index('<text xml:id="tc">')
tl_start = text.index('<text xml:id="tl">')
def layer_at(pos): return "tc" if tc_start <= pos < tl_start else ("tl" if pos >= tl_start else "hdr")
pbs = [(m.start(), m.group(1)) for m in re.finditer(r'<pb facs="#(f\d+)"', text)]
def folio_at(pos):
    cur = None
    for p, f in pbs:
        if p <= pos: cur = f
        else: break
    return cur

# --- segs and divs -----------------------------------------------------------
seg_re = re.compile(r'<seg ana="([^"]+)">(.*?)</seg>', re.S)
segs = []  # (start, end, [ids], cleaned_content)
for m in seg_re.finditer(text):
    ids = [t.lstrip("#") for t in m.group(1).split()]
    content = re.sub(r"<[^>]+>", " ", m.group(2))
    content = re.sub(r"\s+", " ", content).strip().strip("=").strip()
    segs.append((m.start(), m.end(), ids, content))

div_re = re.compile(r'<div ana="([^"]+)">')
divs = []  # (start, end, [ids])
for m in div_re.finditer(text):
    end = text.index("</div>", m.end())
    divs.append((m.start(), end, [t.lstrip("#") for t in m.group(1).split()]))

# usage stats
seg_count = defaultdict(lambda: {"tc": 0, "tl": 0})
seg_folios = defaultdict(list)
spellings = defaultdict(set)
for s, e, ids, content in segs:
    lay, fol = layer_at(s), folio_at(s)
    for cid in ids:
        seg_count[cid][lay] += 1
        if fol and fol not in seg_folios[cid]: seg_folios[cid].append(fol)
        c = norm(content)
        if len(c) >= 4: spellings[cid].add(c)
div_count = defaultdict(int)
for s, e, ids in divs:
    for cid in ids: div_count[cid] += 1

# supplement spellings from catDesc labels + parenthesized originals
for cid, (label, _) in cats.items():
    base = re.sub(r"\s*\([^)]*\)", "", label).strip()
    if len(base) >= 4: spellings[cid].add(norm(base))
    for par in re.findall(r"\(([^)]+)\)", label):
        for piece in re.split(r"[,/]", par):
            p = piece.strip()
            if len(p) >= 4 and not any(w in p for w in ("unidentified", "incl.")):
                spellings[cid].add(norm(p))

# --- masked text for untagged search ----------------------------------------
masked = list(norm(text))
for s, e, _, _ in segs:
    for i in range(s, e): masked[i] = "\x00"
for i in range(0, tc_start):  # mask header + facsimile
    masked[i] = "\x00"
for m in re.finditer(r"<[^>]*>", text):  # mask all markup incl. attribute values
    for i in range(m.start(), m.end()): masked[i] = "\x00"
masked = "".join(masked)

# drop spellings attested under 2+ categories (ambiguous) — list them instead
owners = defaultdict(set)
for cid, sps in spellings.items():
    for sp in sps: owners[sp].add(cid)
ambiguous = {sp for sp, cs in owners.items() if len(cs) > 1}
for cid in spellings: spellings[cid] -= ambiguous

hits = []  # (cid, spelling, folio, layer, class, snippet)
dropped_generic = []
for cid, sps in spellings.items():
    mnum, mlabel = minted[cid]
    for sp in sorted(sps, key=len, reverse=True):
        pat = re.compile(r"(?<!\w)" + re.escape(sp) + r"(?!\w)")
        found = []
        for m in pat.finditer(masked):
            fol = folio_at(m.start())
            if not fol: continue
            fc = folio_chunk(fol)
            cls = "retroactive" if mnum > fc else "possible-miss"
            snippet = re.sub(r"<[^>]+>|\x00+", " ", text[max(0, m.start()-40):m.end()+40])
            snippet = re.sub(r"\s+", " ", snippet).strip()
            found.append((cid, sp, fol, layer_at(m.start()), cls, snippet))
        if len(found) > 15:
            dropped_generic.append((cid, sp, len(found)))
        else:
            hits.extend(found)

# --- structural checks --------------------------------------------------------
union_viol = []   # seg tag not in enclosing div ana
divonly = defaultdict(list)  # div tags with no local seg
for ds, de, dids in divs:
    inner = [(s, e, ids) for s, e, ids, _ in segs if ds < s < de]
    inner_ids = set(i for _, _, ids in inner for i in ids)
    fol, lay = folio_at(ds), layer_at(ds)
    for _, _, ids in inner:
        for i in ids:
            if i not in dids: union_viol.append((fol, lay, i))
    for d in dids:
        if d not in inner_ids: divonly[(fol, lay)].append(d)

parity = []  # folio-level tc vs tl union mismatches
by_folio = defaultdict(lambda: {"tc": set(), "tl": set()})
for ds, de, dids in divs:
    by_folio[folio_at(ds)][layer_at(ds)].update(dids)
tc_only = {"f122", "f123", "f144"}
for fol, d in sorted(by_folio.items()):
    if fol in tc_only: continue
    if d["tc"] != d["tl"]:
        parity.append((fol, sorted(d["tc"] - d["tl"]), sorted(d["tl"] - d["tc"])))

# --- write TAXONOMY_REVIEW.md -------------------------------------------------
out = ["<!-- Generated by the mechanical pre-audit script; regenerate rather than hand-edit the tables. -->",
       "", "# Taxonomy Review Table", "",
       "One row per category, for editor sign-off. `segs` counts tagged occurrences",
       "(transcription+translation); `entries` counts recipe entries carrying the tag;",
       "`minted` is the tagging batch that introduced the category.", ""]
for gid in ["materials", "tools", "measurements", "techniques", "flowers"]:
    members = [(cid, l) for cid, (l, g) in cats.items() if g == gid]
    out += [f"## {gid.capitalize()} ({len(members)})", "",
            "| id | label | segs tc/tl | entries | example folios | minted |",
            "|---|---|---|---|---|---|"]
    for cid, label in sorted(members):
        sc = seg_count[cid]
        ex = ", ".join(seg_folios[cid][:3]) or "—"
        out.append(f"| `{cid}` | {label} | {sc['tc']}/{sc['tl']} | {div_count[cid]} | {ex} | {minted[cid][1]} |")
    out.append("")
unused = [cid for cid in cats if div_count[cid] == 0 and seg_count[cid]["tc"] + seg_count[cid]["tl"] == 0]
out += ["## Possible merge candidates (for editorial decision)", "",
        "- `sap_green` vs `bouck_green` — both unidentified green pigments (sap groen / boūck groen)",
        "- `pot` vs `earthenware_pot` vs `marmite` vs `terrine` — vessel granularity",
        "- `marble_slab` — manuscript twice offers sandstone (*grez*) as alternative; widen to 'stone slab'?",
        "- `brazilwood` vs `logwood` — pending the translation-inversion ruling (see EDITORIAL_QUESTIONS.md)",
        "- `toile` vs `cloth` vs `muslin`/`cambric` — check application consistency",
        "", f"## Unused categories: {', '.join(sorted(unused)) if unused else 'none'}", ""]
open(f"{REPO}/TAXONOMY_REVIEW.md", "w").write("\n".join(out))

# --- write PREAUDIT_CANDIDATES.md ----------------------------------------------
retro = [h for h in hits if h[4] == "retroactive"]
miss = [h for h in hits if h[4] == "possible-miss"]
out = ["<!-- Generated by the mechanical pre-audit script. Candidates only - a string hit is not a semantic hit; adjudicate against TAGGING_DECISIONS.md precedents. -->",
       "", "# Pre-audit: Untagged Occurrences of Known Category Spellings", "",
       f"Total candidates: **{len(hits)}** — {len(retro)} retroactive (category minted after the",
       f"folio's batch was tagged), {len(miss)} possible misses (category existed; may be a",
       "deliberate skip under the back-reference / color-name / non-recipe precedents).", ""]
for title, rows in [("Retroactive candidates", retro), ("Possible misses", miss)]:
    out += [f"## {title} ({len(rows)})", "", "| category | spelling | folio | layer | context |", "|---|---|---|---|---|"]
    percat = defaultdict(int)
    for cid, sp, fol, lay, _, snip in sorted(rows):
        percat[cid] += 1
        if percat[cid] <= 8:
            out.append(f"| `{cid}` | {sp} | {fol} | {lay} | …{snip[:90]}… |")
    extra = {c: n - 8 for c, n in percat.items() if n > 8}
    if extra:
        out.append("")
        out.append("Truncated: " + ", ".join(f"`{c}` +{n} more" for c, n in sorted(extra.items())))
    out.append("")
out += ["## Structural checks", "",
        f"- Union-rule violations (seg tag missing from its div's ana): **{len(union_viol)}**"]
for fol, lay, i in union_viol[:20]:
    out.append(f"  - {fol} {lay}: `#{i}`")
out += [f"- Folio-level tc/tl parity mismatches: **{len(parity)}**"]
for fol, tconly, tlonly in parity[:20]:
    out.append(f"  - {fol}: tc-only {tconly} / tl-only {tlonly}")
ndivonly = sum(len(v) for v in divonly.values())
out += [f"- Div-level tags with no local seg: **{ndivonly}** (many are legitimate rule-5 /",
        "  union cases; list available on request)", "",
        "## Dropped from the search (not silently)", "",
        "Ambiguous spellings attested under 2+ categories (excluded entirely): " +
        (", ".join(sorted(ambiguous)) if ambiguous else "none"), ""]
if dropped_generic:
    out += ["Generic spellings with >15 untagged hits (excluded as noise; recheck manually if",
            "any looks specific):", ""]
    for cid, sp, n in sorted(dropped_generic, key=lambda x: -x[2]):
        out.append(f"- `{cid}` · \"{sp}\" · {n} hits")
    out.append("")
open(f"{REPO}/PREAUDIT_CANDIDATES.md", "w").write("\n".join(out))

print(f"categories={len(cats)} segs={len(segs)} divs={len(divs)}")
print(f"retroactive={len(retro)} possible_miss={len(miss)} union_viol={len(union_viol)} parity={len(parity)} unused={len(unused)}")
