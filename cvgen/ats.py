"""Deterministic ATS analysis - no model involved, so the score is reproducible."""
import re
from collections import Counter
from .models import clean
STOP = set("a an the and or of to in for with on at by from as is are be this that will you your we our their it its they have has had not but can may should must such than then also into over per via etc able about all any more most other some who what when where which while within would including strong experience work working team teams role years year ability skills plus essential need needed building required preferred looking seeking join strongly".split())
WEAK = ("responsible for", "worked on", "helped", "assisted", "duties included", "tasked with")

def cv_text(cv):
    c = clean(cv); p = [c["headline"], c["summary"], " ".join(c["skills"]), " ".join(c["certifications"])]
    for e in c["experience"]: p += [e["role"], e["company"], " ".join(e["bullets"])]
    for e in c["education"]: p += [e["degree"], e["school"], e["details"]]
    for e in c["projects"]: p += [e["name"], e["description"], e["tech"]]
    return " ".join(p).lower()

def keywords(jd, n=24):
    toks = re.findall(r"[A-Za-z][A-Za-z0-9+#.\-]*", jd); low = [t.lower().strip(".-") for t in toks]
    uni = Counter(); 
    for t, l in zip(toks, low):
        if l not in STOP and len(l) > 2: uni[l] += 1 + (1 if re.search(r"[+#.\d]|^[A-Z]{2,}", t) else 0)
    bi = Counter(f"{a} {b}" for a, b in zip(low, low[1:]) if a not in STOP and b not in STOP and len(a) > 2 and len(b) > 2)
    pick = [(k, v * 1.5) for k, v in bi.items() if v >= 2] + list(uni.items())
    out = []
    for k, _ in sorted(pick, key=lambda x: -x[1]):
        if any(k != o and (k in o.split() or o in k.split()) for o in out): continue
        out.append(k)
        if len(out) == n: break
    return out

def analyse(cv, jd=""):
    c = clean(cv); txt = cv_text(cv); bullets = [b for e in c["experience"] for b in e["bullets"]]
    checks = [("Email present", bool(re.match(r"[^@\s]+@[^@\s]+\.\w+", c["email"]))), ("Phone present", len(re.sub(r"\D", "", c["phone"])) >= 7), ("Location present", bool(c["location"])),
              ("Summary of 40-120 words", 40 <= len(c["summary"].split()) <= 120), ("Experience with 2+ bullets", any(len(e["bullets"]) >= 2 for e in c["experience"])),
              ("Education listed", any(e["school"] for e in c["education"])), ("6+ skills listed", len(c["skills"]) >= 6), ("Dates on every role", all(e["start"] for e in c["experience"]) and bool(c["experience"]))]
    structure = round(100 * sum(ok for _, ok in checks) / len(checks)); tips = [f"Fix: {n}" for n, ok in checks if not ok]
    weak = sum(any(b.lower().startswith(w) for w in WEAK) for b in bullets); fp = sum(bool(re.search(r"\b(i|my|me)\b", b.lower())) for b in bullets)
    quant = sum(bool(re.search(r"\d", b)) for b in bullets) / max(1, len(bullets)); avg = sum(len(b.split()) for b in bullets) / max(1, len(bullets))
    hyg = 100 - min(40, weak * 10) - min(20, fp * 10) - (0 if quant >= .3 else 20) - (0 if 8 <= avg <= 28 or not bullets else 20); hyg = max(0, hyg)
    if weak: tips.append(f"{weak} bullet(s) open with weak phrases such as 'responsible for' - lead with an action verb.")
    if fp: tips.append("Remove first-person pronouns from bullets.")
    if bullets and quant < .3: tips.append("Fewer than 30% of bullets contain numbers - add scale, time or outcome metrics you can verify.")
    if bullets and not 8 <= avg <= 28: tips.append(f"Average bullet length is {avg:.0f} words; aim for 12-25.")
    kws = keywords(jd) if jd.strip() else []; found = [k for k in kws if re.search(r"(?<![a-z0-9])" + re.escape(k) + r"(?![a-z0-9])", txt)]
    cov = round(100 * len(found) / len(kws)) if kws else None
    score = round(.5 * cov + .3 * structure + .2 * hyg) if kws else round(.6 * structure + .4 * hyg)
    if kws and cov < 60: tips.append("Keyword coverage is below 60% - use 'Tailor with AI' or work the missing terms in where they are truthful.")
    return dict(score=score, structure=structure, hygiene=hyg, coverage=cov, found=found, missing=[k for k in kws if k not in found], checks=checks, tips=tips, with_jd=bool(kws))
