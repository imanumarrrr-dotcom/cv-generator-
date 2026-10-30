import copy, uuid
from typing import List
from pydantic import BaseModel, ConfigDict

class S(BaseModel): model_config = ConfigDict(extra="forbid")
class Link(S): label: str; url: str
class Exp(S): company: str; role: str; location: str; start: str; end: str; bullets: List[str]
class Edu(S): school: str; degree: str; location: str; start: str; end: str; details: str
class Proj(S): name: str; link: str; description: str; tech: str
class CV(S):
    name: str; headline: str; email: str; phone: str; location: str; links: List[Link]; summary: str
    experience: List[Exp]; education: List[Edu]; skills: List[str]; projects: List[Proj]; certifications: List[str]; languages: List[str]
class Tailored(S): cv: CV; changes: List[str]; keywords_used: List[str]; suggestions: List[str]
class Improved(S): bullets: List[str]; suggestions: List[str]
class Text(S): text: str
class Variants(S): headline: str; about: str; tagline: str
class QA(S): question: str; why_asked: str; tip: str
class Questions(S): items: List[QA]

EMPTY = dict(name="", headline="", email="", phone="", location="", links=[], summary="", experience=[], education=[], skills=[], projects=[], certifications=[], languages=[])
BLANK = dict(experience=dict(company="", role="", location="", start="", end="", bullets=[]), education=dict(school="", degree="", location="", start="", end="", details=""),
             projects=dict(name="", link="", description="", tech=""))

def new_item(kind): d = copy.deepcopy(BLANK[kind]); d["_id"] = uuid.uuid4().hex[:6]; return d
def with_ids(cv):
    cv = copy.deepcopy({**EMPTY, **cv})
    for k in BLANK:
        cv[k] = [{**BLANK[k], **i, "_id": uuid.uuid4().hex[:6]} for i in cv[k]]
    return cv
def clean(cv):
    out = copy.deepcopy(cv)
    for k in BLANK: out[k] = [{kk: vv for kk, vv in i.items() if not kk.startswith("_")} for i in out[k]]
    for k in ("skills", "certifications", "languages"): out[k] = [s.strip() for s in out[k] if s.strip()]
    for e in out["experience"]: e["bullets"] = [b.strip() for b in e["bullets"] if b.strip()]
    return out
def completeness(cv):
    c = clean(cv); chk = [c["name"], c["headline"], c["email"], c["phone"], c["location"], len(c["summary"]) > 80, any(e["role"] and e["bullets"] for e in c["experience"]),
                          any(e["school"] for e in c["education"]), len(c["skills"]) >= 6, bool(c["projects"] or c["certifications"])]
    return round(100 * sum(bool(x) for x in chk) / len(chk))
