"""Animated themes. Colours are registered with @property so a theme switch cross-fades smoothly (Chromium/Edge/Safari)."""
THEMES = {  # bg1, bg2, bg3, card, text, muted, accent, accent2, border
 "Human Next":    ("#0A0A0A", "#0A1822", "#1A0A16", "rgba(255,255,255,.05)", "#F4F7FB", "#8FA3B8", "#2FB0E3", "#FF2D95", "rgba(255,255,255,.12)"),
 "Cerulean Deep": ("#050B10", "#00334A", "#0A0A0A", "rgba(0,123,167,.14)", "#EAF8FF", "#7FB5CC", "#19C3E6", "#FF2D95", "rgba(47,176,227,.28)"),
 "Rose Noir":     ("#0A0A0A", "#26081A", "#0B1E2B", "rgba(255,45,149,.09)", "#FFF1F8", "#C79AB3", "#FF2D95", "#3DB8E8", "rgba(255,45,149,.30)"),
 "Paper":         ("#F5F8FB", "#E6F1F7", "#FCEFF6", "rgba(255,255,255,.80)", "#0A0A0A", "#4D5C6B", "#007BA7", "#E0207F", "rgba(0,0,0,.14)")}
P = ["bg1", "bg2", "bg3", "card", "text", "muted", "accent", "accent2", "border"]

def css(name, sweep):
    v = dict(zip(P, THEMES[name])); reg = "".join(f"@property --{p}{{syntax:'<color>';inherits:true;initial-value:#000}}" for p in P)
    root = ":root{" + "".join(f"--{p}:{v[p]};" for p in P) + "transition:" + ",".join(f"--{p} .9s ease" for p in P) + "}"
    return "<style>@import url('https://fonts.googleapis.com/css2?family=Michroma&family=Manrope:wght@400;600;800&family=JetBrains+Mono&display=swap');" + reg + root + f"""
html,body,.stApp{{font-family:'Manrope',system-ui,sans-serif}}
.stApp{{background:linear-gradient(135deg,var(--bg1),var(--bg2) 55%,var(--bg3));color:var(--text)}}
.stApp::before{{content:"";position:fixed;inset:-25%;pointer-events:none;z-index:0;opacity:.20;filter:blur(30px);
 background:radial-gradient(34% 30% at 18% 22%,var(--accent) 0,transparent 70%),radial-gradient(30% 28% at 82% 72%,var(--accent2) 0,transparent 70%);animation:drift 24s ease-in-out infinite alternate}}
@keyframes drift{{from{{transform:translate3d(-3%,-2%,0) scale(1)}}to{{transform:translate3d(4%,3%,0) scale(1.15)}}}}
.sweep{{position:fixed;inset:0;z-index:9999;pointer-events:none;background:linear-gradient(100deg,transparent 35%,var(--accent) 48%,var(--accent2) 52%,transparent 65%);opacity:0;animation:sweep{sweep} .9s ease-out}}
@keyframes sweep0{{from{{transform:translateX(-100%);opacity:.55}}to{{transform:translateX(100%);opacity:0}}}}@keyframes sweep1{{from{{transform:translateX(-100%);opacity:.55}}to{{transform:translateX(100%);opacity:0}}}}
.stApp p,.stApp label,.stApp li,.stApp span,.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp summary,[data-testid="stMetricValue"],[data-testid="stMetricLabel"]{{color:var(--text)}}
[data-testid="stCaptionContainer"],.stCaption{{color:var(--muted)!important}}[data-testid="stHeader"]{{background:transparent}}
[data-testid="stSidebar"]{{background:var(--card);backdrop-filter:blur(16px);border-right:1px solid var(--border)}}.block-container{{position:relative;z-index:1;padding-top:2rem;max-width:1250px}}
.eyebrow{{font:600 .72rem 'Manrope';letter-spacing:.38em;color:var(--muted);text-transform:uppercase;margin-bottom:.6rem}}
.hero{{font:400 clamp(2.4rem,6vw,4.6rem)/1.02 'Michroma',sans-serif;letter-spacing:.01em}}
.hero .l1{{display:block;background:linear-gradient(90deg,var(--accent),#7fd3f7);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 22px color-mix(in srgb,var(--accent) 45%,transparent))}}
.hero .l2{{display:block;background:linear-gradient(90deg,var(--accent2),#ff7ac0);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 22px color-mix(in srgb,var(--accent2) 55%,transparent))}}
.tag{{font:600 .7rem 'Manrope';letter-spacing:.34em;color:var(--muted);text-transform:uppercase;margin:1rem 0 1.4rem}}.tag b{{color:var(--accent2);font-weight:600}}
.rise{{animation:rise .8s cubic-bezier(.2,.8,.2,1) both}}@keyframes rise{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:none}}}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:1.1rem 1.3rem;backdrop-filter:blur(12px);margin-bottom:.8rem}}
.topline{{height:1px;background:linear-gradient(90deg,var(--accent),var(--accent2),transparent);margin:.2rem 0 1.2rem}}
[data-testid="stMetric"]{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:.7rem 1rem;transition:border-color .3s,transform .3s}}[data-testid="stMetric"]:hover{{border-color:var(--accent2);transform:translateY(-2px)}}
[data-testid="stMetricLabel"] p{{letter-spacing:.2em;font-size:.68rem;text-transform:uppercase;color:var(--muted)}}
.stButton>button,.stDownloadButton>button{{border-radius:999px;border:1px solid var(--border);background:var(--card);color:var(--text);transition:all .25s;letter-spacing:.04em}}
.stButton>button:hover,.stDownloadButton>button:hover{{border-color:var(--accent2);box-shadow:0 0 0 3px color-mix(in srgb,var(--accent2) 28%,transparent),0 0 22px color-mix(in srgb,var(--accent2) 35%,transparent);transform:translateY(-1px)}}
.stButton>button[kind="primary"]{{background:linear-gradient(90deg,#007BA7,var(--accent2));color:#fff;border:0;font-weight:700}}
.stTabs [data-baseweb="tab-list"]{{gap:.2rem;border-bottom:1px solid var(--border)}}.stTabs [data-baseweb="tab"]{{border-radius:12px 12px 0 0;color:var(--muted);letter-spacing:.06em;transition:all .3s}}
.stTabs [aria-selected="true"]{{color:var(--text);background:var(--card)}}.stTabs [data-baseweb="tab-highlight"]{{background:linear-gradient(90deg,var(--accent),var(--accent2));height:3px}}
[data-baseweb="input"],[data-baseweb="textarea"],[data-baseweb="select"]>div,[data-testid="stNumberInputContainer"]{{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:12px!important}}
[data-baseweb="base-input"]{{background:transparent!important}}input,textarea{{color:var(--text)!important;-webkit-text-fill-color:var(--text)!important;caret-color:var(--accent2)!important}}
input::placeholder,textarea::placeholder{{color:var(--muted)!important;-webkit-text-fill-color:var(--muted)!important;opacity:.85}}
[data-baseweb="input"]:focus-within,[data-baseweb="textarea"]:focus-within{{border-color:var(--accent2)!important;box-shadow:0 0 0 3px color-mix(in srgb,var(--accent2) 25%,transparent)}}
[data-baseweb="select"] *{{color:var(--text)!important}}[data-baseweb="popover"] ul,[data-baseweb="menu"]{{background:var(--bg2)!important}}[data-baseweb="popover"] li,[data-baseweb="popover"] li *{{color:var(--text)!important}}
[data-testid="stExpander"] details{{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:14px}}[data-testid="stExpander"] summary,[data-testid="stExpander"] summary *{{color:var(--text)!important;background:transparent!important}}
[data-testid="stFileUploaderDropzone"]{{background:var(--card)!important;border:1px dashed var(--border)!important}}[data-testid="stFileUploader"] *{{color:var(--text)!important}}
[data-testid="stAlert"]{{background:var(--card);border:1px solid var(--border);border-radius:14px}}
.chip{{display:inline-block;margin:0 6px 6px 0;padding:3px 11px;border-radius:999px;font-size:.75rem;border:1px solid var(--border)}}.ok{{border-color:var(--accent);color:var(--accent)}}.miss{{border-color:var(--accent2);color:var(--accent2)}}
.ring{{width:150px;height:150px;border-radius:50%;display:grid;place-items:center;margin:auto;background:conic-gradient(var(--accent) calc(var(--p)*1%),var(--accent2) calc(var(--p)*1%) calc(var(--p)*1% + 0.01%),rgba(128,128,128,.2) 0);transition:--p 1s}}
.ring div{{width:118px;height:118px;border-radius:50%;background:var(--bg1);display:grid;place-items:center;font:400 2rem 'Michroma',sans-serif}}
.bar{{height:8px;border-radius:8px;background:rgba(128,128,128,.22);overflow:hidden;margin:.2rem 0 .8rem}}.bar i{{display:block;height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2));border-radius:8px}}
.pulse{{display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--accent2);margin-right:8px;animation:pulse 1.6s infinite}}@keyframes pulse{{0%{{box-shadow:0 0 0 0 var(--accent2)}}100%{{box-shadow:0 0 0 12px transparent}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}}}</style><div class="sweep"></div>"""
