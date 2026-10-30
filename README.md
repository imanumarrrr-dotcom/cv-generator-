# CVForge AI (Streamlit)
AI CV builder: import an old CV, tailor it to a job description, score it for ATS, and export PDF / DOCX / HTML / Markdown / JSON.
Palette: Jet Black `#0A0A0A`, Cerulean `#007BA7`, Neon Rose `#FF2D95`; four animated themes with cross-fade transitions.

```
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
Enter your OpenAI key on the first screen (session memory only), or set `OPENAI_API_KEY` and click "Use environment key".

- **Truthfulness guard:** prompts forbid inventing employers, dates, degrees, skills or metrics; tailoring is shown as a before/after diff and applied only on click (Undo available).
- **ATS score:** computed in code (keyword coverage, structure, writing hygiene), so it is repeatable. Not a guarantee of how any real ATS will rank you.
- **Privacy:** the CV text is sent to OpenAI when you use AI features. Nothing is stored on disk except files you download.
- Models are selectable in the sidebar; verify model names against current OpenAI docs.
