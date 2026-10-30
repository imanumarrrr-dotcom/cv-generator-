import io, json, os, time
import streamlit as st, streamlit.components.v1 as components
from cvgen import ai as A, ats, render, theme
from cvgen.demo import DEMO
from cvgen.models import EMPTY, clean, completeness, new_item, with_ids

st.set_page_config(page_title="CVForge AI", page_icon="◆", layout="wide")
ss = st.session_state
MODELS = ["gpt-4o-mini", "gpt-4.1-mini", "gpt-4.1", "gpt-4o"]

def paint():
    if ss.get("last_theme") != ss.get("theme", "Human Next"): ss.sweep = 1 - ss.get("sweep", 1); ss.last_theme = ss.get("theme", "Human Next")
    st.markdown(theme.css(ss.get("theme", "Human Next"), ss.get("sweep", 0)), unsafe_allow_html=True)

# ───────────── key gate ─────────────
def gate():
    paint(); l, r = st.columns([1.25, 1], gap="large")
    with l:
        st.markdown('<div class="rise"><div class="eyebrow">A sharper career story</div><div class="hero"><span class="l1">CV</span><span class="l2">FORGE</span></div>'
                    '<div class="tag">Where experience meets <b>intelligence</b></div></div>', unsafe_allow_html=True)
        st.markdown("**Build, tailor and export an ATS-ready CV.** Import an old CV, match it to any job description, and get a cover letter and interview prep, without the AI ever inventing a job, a degree or a number.")
        st.caption("Truthfulness guard · reproducible ATS score · PDF, DOCX, HTML, Markdown, JSON")
    with r:
        st.markdown('<div class="card rise"><div class="eyebrow">Access console</div>', unsafe_allow_html=True)
        key = st.text_input("OpenAI API key", type="password", placeholder="sk-…", help="Held in this browser session only; never saved to disk. Use a project key with a spend limit.")
        a, b = st.columns(2); env = bool(os.getenv("OPENAI_API_KEY")) and b.button("Use environment key")
        if a.button("Open console  →", type="primary") or env:
            k = os.getenv("OPENAI_API_KEY") if env else key.strip()
            if not k: st.error("Enter a key to continue.")
            else:
                with st.status("Verifying key…", expanded=True) as s:
                    err = A.connect(k)
                    if err: s.update(label="Verification failed", state="error"); st.error(err)
                    else:
                        for m in ("Key accepted", "Loading templates", "Arming truthfulness guard", "Opening console"): st.write("✓ " + m); time.sleep(.3)
                        ss.key = k; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ───────────── helpers ─────────────
def snap(note): ss.history = (ss.history + [(time.strftime("%H:%M:%S"), note, json.dumps(clean(ss.cv)))])[-8:]
def set_cv(cv, note): snap(note); ss.cv = with_ids(cv); ss.reset = True; st.rerun()
def ai(): return A.AI(ss.key, ss.model, ss.usage)
def run(fn, label):
    try:
        with st.spinner(label): return fn()
    except A.AIError as e: st.error(str(e)); return None
def bar(label, v): st.markdown(f'<div style="display:flex;justify-content:space-between"><span>{label}</span><b>{v}%</b></div><div class="bar"><i style="width:{v}%"></i></div>', unsafe_allow_html=True)
def read_upload(f):
    n = f.name.lower(); b = f.read()
    if n.endswith(".pdf"):
        from pypdf import PdfReader; return "\n".join(p.extract_text() or "" for p in PdfReader(io.BytesIO(b)).pages)
    if n.endswith(".docx"):
        import docx; return "\n".join(p.text for p in docx.Document(io.BytesIO(b)).paragraphs)
    return b.decode("utf-8", "ignore")

def lines(label, key, items): return [x.strip() for x in st.text_area(label, "\n".join(items), key=key, height=90).splitlines() if x.strip()]

def editor(kind, title, fields, big=None):
    cv = ss.cv
    for it in list(cv[kind]):
        u = it["_id"]; head = it.get(fields[0][0]) or "New entry"
        with st.expander(f"{title}: {head}", expanded=not it.get(fields[0][0])):
            cols = st.columns(len(fields))
            for c, (f, lab) in zip(cols, fields): it[f] = c.text_input(lab, it[f], key=f"x_{u}_{f}")
            if kind == "experience":
                if st.button("✨ Strengthen bullets", key=f"x_{u}_imp") and it["bullets"]:
                    r = run(lambda: ai().improve(f'{it["role"]} at {it["company"]}', it["bullets"], ss.tone), "Rewriting bullets…")
                    if r: ss[f"x_{u}_b"] = "\n".join(r.bullets); ss.tips = r.suggestions
                it["bullets"] = [x.strip() for x in st.text_area("Achievements (one per line)", "\n".join(it["bullets"]), key=f"x_{u}_b", height=130).splitlines() if x.strip()]
            else: it[big[0]] = st.text_area(big[1], it[big[0]], key=f"x_{u}_{big[0]}", height=80)
            if st.button("Remove", key=f"x_{u}_rm"): cv[kind] = [x for x in cv[kind] if x["_id"] != u]; st.rerun()
    if st.button(f"＋ Add {title.lower()}", key=f"add_{kind}"): cv[kind].append(new_item(kind)); st.rerun()

# ───────────── console ─────────────
def console():
    ss.setdefault("cv", with_ids(EMPTY)); ss.setdefault("history", []); ss.setdefault("usage", dict({"in": 0, "out": 0, "calls": 0})); ss.setdefault("model", MODELS[0]); ss.setdefault("tone", "Professional")
    if ss.pop("reset", False):
        for k in [k for k in ss if k.startswith(("x_", "p_"))]: del ss[k]
    with st.sidebar:
        st.markdown(f'<span class="pulse"></span>**Connected** · `{ss.key[:3]}…{ss.key[-4:]}`', unsafe_allow_html=True)
        if st.button("Disconnect"):
            for k in list(ss): del ss[k]
            st.rerun()
        st.selectbox("🎨 Theme", list(theme.THEMES), key="theme"); st.selectbox("Model", MODELS, key="model"); st.selectbox("Writing tone", list(A.TONES), key="tone")
        u = ss.usage; st.caption(f"{u['calls']} AI calls · {u['in']:,} in / {u['out']:,} out tokens")
        st.divider(); st.download_button("⬇ Save profile (JSON)", render.to_json(ss.cv), "cv_profile.json", use_container_width=True)
        up = st.file_uploader("Load profile JSON", type="json", key="pj")
        if up and st.button("Load profile", use_container_width=True): set_cv(json.loads(up.read()), "Loaded profile")
        if ss.history and st.button("↶ Undo last change", use_container_width=True):
            ss.cv = with_ids(json.loads(ss.history.pop()[2])); ss.reset = True; st.rerun()
        if st.button("Clear everything", use_container_width=True): set_cv(EMPTY, "Cleared")
    paint(); cv = ss.cv; res = ats.analyse(cv, ss.get("jd", ""))
    st.markdown('<div class="eyebrow">CVForge AI · console</div><div class="hero" style="font-size:2.4rem"><span class="l1" style="display:inline">CV</span><span class="l2" style="display:inline"> FORGE</span></div><div class="topline"></div>', unsafe_allow_html=True)
    m = st.columns(4); m[0].metric("Completeness", f"{completeness(cv)}%"); m[1].metric("ATS score", res["score"]); m[2].metric("Keyword match", f'{res["coverage"]}%' if res["coverage"] is not None else "—"); m[3].metric("History", len(ss.history))
    T = st.tabs(["🧬 Profile", "🎯 Job match", "✨ AI studio", "📊 ATS check", "🖼 Preview & export"])

    with T[0]:
        a, b, c = st.columns(3)
        with a:
            f = st.file_uploader("Import existing CV (PDF, DOCX, TXT)", type=["pdf", "docx", "txt", "md"], key="imp")
            if f and st.button("Parse with AI", type="primary"):
                txt = read_upload(f)
                if len(txt.strip()) < 80: st.error("Couldn't read text from that file (scanned PDFs need OCR).")
                else:
                    r = run(lambda: ai().extract(txt), "Reading your CV…")
                    if r: set_cv(r, "Imported CV")
        with b:
            st.write(""); st.write("")
            if st.button("Load demo profile"): set_cv(DEMO, "Demo profile")
        with c: st.caption("AI import only extracts what your file says. Review each section after importing.")
        with st.expander("Basics", expanded=True):
            x = st.columns(2)
            cv["name"] = x[0].text_input("Full name", cv["name"], key="p_name"); cv["headline"] = x[1].text_input("Headline", cv["headline"], key="p_hl", placeholder="Data Analyst | SQL, Python")
            y = st.columns(3); cv["email"] = y[0].text_input("Email", cv["email"], key="p_em"); cv["phone"] = y[1].text_input("Phone", cv["phone"], key="p_ph"); cv["location"] = y[2].text_input("Location", cv["location"], key="p_lo")
            raw = st.text_area("Links (one per line: Label | URL)", "\n".join(f'{l["label"]} | {l["url"]}' for l in cv["links"]), key="p_links", height=80)
            cv["links"] = [dict(label=p[0].strip(), url=p[-1].strip()) if len(p) > 1 else dict(label="", url=p[0].strip()) for p in (l.split("|") for l in raw.splitlines() if l.strip())]
        with st.expander("Summary", expanded=True):
            if st.button("✨ Write summary with AI"):
                t = run(lambda: ai().summary(cv, ss.tone), "Writing…")
                if t: ss.p_sum = t
            cv["summary"] = st.text_area("Professional summary", cv["summary"], key="p_sum", height=110)
        editor("experience", "Role", [("role", "Role"), ("company", "Company"), ("location", "Location"), ("start", "Start"), ("end", "End")])
        editor("education", "Education", [("degree", "Degree"), ("school", "School"), ("location", "Location"), ("start", "Start"), ("end", "End")], ("details", "Details"))
        editor("projects", "Project", [("name", "Name"), ("link", "Link"), ("tech", "Tech")], ("description", "Description"))
        with st.expander("Skills, certifications, languages"):
            cv["skills"] = [s.strip() for s in st.text_area("Skills (comma separated)", ", ".join(cv["skills"]), key="p_sk").split(",") if s.strip()]
            z = st.columns(2); 
            with z[0]: cv["certifications"] = lines("Certifications (one per line)", "p_ce", cv["certifications"])
            with z[1]: cv["languages"] = lines("Languages (one per line)", "p_la", cv["languages"])
        if ss.get("tips"): st.info("Suggestions: " + " · ".join(ss.tips))

    with T[1]:
        l, r = st.columns([1.2, 1])
        with l:
            st.text_area("Paste the job description", key="jd", height=260, placeholder="Paste the full job post here…")
            q = st.columns(2); co = q[0].text_input("Company", key="co"); ro = q[1].text_input("Target role", key="ro")
            if st.button("Tailor my CV with AI", type="primary") and ss.get("jd", "").strip():
                t = run(lambda: ai().tailor(cv, ss.jd, ss.tone), "Tailoring (rewording only, no invention)…")
                if t: ss.tailored = t.model_dump()
            elif not ss.get("jd", "").strip(): st.caption("Add a job description to enable matching.")
        with r:
            if res["with_jd"]:
                bar("Keyword coverage", res["coverage"]); st.markdown("**Found** " + "".join(f'<span class="chip ok">{k}</span>' for k in res["found"]), unsafe_allow_html=True)
                st.markdown("**Missing** " + "".join(f'<span class="chip miss">{k}</span>' for k in res["missing"]), unsafe_allow_html=True); st.caption("Only add a missing keyword if it is true for you.")
            else: st.markdown('<div class="card">Paste a job description to see an instant, model-free keyword match.</div>', unsafe_allow_html=True)
        t = ss.get("tailored")
        if t:
            st.markdown("#### Proposed changes"); st.markdown("\n".join(f"- {c}" for c in t["changes"]))
            d = st.columns(2); d[0].markdown("**Current summary**"); d[0].write(cv["summary"] or "—"); d[1].markdown("**Tailored summary**"); d[1].write(t["cv"]["summary"])
            for old, new in zip(cv["experience"], t["cv"]["experience"]):
                with st.expander(f'Bullets: {new["role"]}'):
                    p = st.columns(2); p[0].markdown("\n".join(f"- {b}" for b in old["bullets"])); p[1].markdown("\n".join(f"- {b}" for b in new["bullets"]))
            if t["suggestions"]: st.info("Gaps to consider: " + " · ".join(t["suggestions"]))
            ok = st.columns(2)
            if ok[0].button("✔ Apply tailored CV", type="primary"): ss.tailored = None; set_cv(t["cv"], "Applied tailored CV")
            if ok[1].button("Discard"): ss.tailored = None; st.rerun()

    with T[2]:
        jd = ss.get("jd", ""); s1, s2, s3 = st.tabs(["Cover letter", "LinkedIn", "Interview prep"])
        with s1:
            if st.button("Generate cover letter", type="primary"):
                ss.letter = run(lambda: ai().cover_letter(cv, jd, ss.get("co", ""), ss.get("ro", ""), ss.tone), "Writing…")
            if ss.get("letter"): ss.letter = st.text_area("Edit freely", ss.letter, height=360); st.download_button("Download .txt", ss.letter, "cover_letter.txt")
        with s2:
            if st.button("Generate LinkedIn copy", type="primary"): ss.li = run(lambda: ai().linkedin(cv, ss.tone), "Writing…")
            if ss.get("li"): st.text_input("Headline", ss.li.headline, key="li_h"); st.text_area("About", ss.li.about, height=200, key="li_a"); st.text_input("Tagline", ss.li.tagline, key="li_t")
        with s3:
            if st.button("Generate interview questions", type="primary"): ss.qa = run(lambda: ai().interview(cv, jd), "Thinking…")
            for i, qa in enumerate(ss.get("qa") or [], 1):
                with st.expander(f"{i}. {qa.question}"): st.markdown(f"**Why they ask:** {qa.why_asked}"); st.markdown(f"**Tip:** {qa.tip}")

    with T[3]:
        l, r = st.columns([1, 1.4])
        with l: st.markdown(f'<div class="ring" style="--p:{res["score"]}"><div>{res["score"]}</div></div><p style="text-align:center" class="tag">{"vs. job description" if res["with_jd"] else "structure only"}</p>', unsafe_allow_html=True)
        with r:
            bar("Structure", res["structure"]); bar("Writing hygiene", res["hygiene"])
            if res["coverage"] is not None: bar("Keyword coverage", res["coverage"])
        st.markdown("#### Checklist"); st.markdown("\n".join(f"- {'✅' if ok else '⬜'} {n}" for n, ok in res["checks"]))
        if res["tips"]: st.markdown("#### What to improve"); st.markdown("\n".join(f"- {t}" for t in res["tips"]))
        st.caption("Scores are computed in code, not by a model, so they are repeatable.")

    with T[4]:
        tp = st.radio("Template", list(render.T), horizontal=True, key="tpl")
        if not cv["name"]: st.warning("Add your name in the Profile tab, or load the demo profile.")
        h = render.to_html(cv, tp); components.html(h, height=1100, scrolling=True)
        d = st.columns(5); nm = (cv["name"] or "cv").replace(" ", "_")
        d[0].download_button("PDF", render.to_pdf(cv, tp), f"{nm}_CV.pdf", "application/pdf", use_container_width=True); d[1].download_button("DOCX", render.to_docx(cv), f"{nm}_CV.docx", use_container_width=True)
        d[2].download_button("HTML", h, f"{nm}_CV.html", "text/html", use_container_width=True); d[3].download_button("Markdown", render.to_md(cv), f"{nm}_CV.md", use_container_width=True); d[4].download_button("JSON", render.to_json(cv), f"{nm}_CV.json", use_container_width=True)
        st.caption("PDF and DOCX use clean, single-column, ATS-friendly layouts; the Human Next dark style is for on-screen and HTML sharing.")

if "key" not in ss:
    gate()
else:
    console()
