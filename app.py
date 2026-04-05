import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LLMRank 2026 — Best LLMs for Coding",
    page_icon="⌨",          
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
#  THEME TOKENS  (dark only)
# ─────────────────────────────────────────────────────────────────────────────
T = dict(
    bg="#09090f", bg2="#111118", bg3="#18181f", border="#2a2a38",
    accent="#7c6af7", accent2="#22d3ee", accent3="#f472b6",
    text="#e8e8f0", muted="#6b6b82", gold="#fbbf24", green="#4ade80",
    shadow="rgba(124,106,247,0.12)",
    ptpl="plotly_dark", paper="#111118", plot="#09090f", grid="#2a2a38",
)

# ─────────────────────────────────────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');

html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main .block-container {{
    background-color: {T['bg']} !important;
    color: {T['text']} !important;
    font-family: 'Syne', sans-serif !important;
}}
.block-container {{ padding-top: 4rem !important; max-width: 1400px !important; }}

/* Header: static position so it never overlaps content, keeps the border */
[data-testid="stHeader"] {{
    position: relative !important;
    background: {T['bg']} !important;
    border-bottom: 1px solid {T['border']} !important;
    z-index: 0 !important;
}}
/* Hide keyboard_double text — target both the header button and sidebar collapse button */
[data-testid="stHeader"] button,
[data-testid="stSidebarCollapseButton"] button,
[data-testid="stSidebarCollapsedControl"] button {{
    font-size: 0 !important;
    color: transparent !important;
    width: 2rem !important;
    height: 2rem !important;
}}
/* The span inside those buttons holds the raw icon text — nuke it */
[data-testid="stHeader"] button span,
[data-testid="stSidebarCollapseButton"] button span,
[data-testid="stSidebarCollapsedControl"] button span,
[data-testid="stSidebarCollapseButton"] button * ,
[data-testid="stSidebarCollapsedControl"] button * {{
    font-size: 0 !important;
    color: transparent !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    display: block !important;
}}
[data-testid="stSidebar"] {{
    background: {T['bg2']} !important;
    border-right: 1px solid {T['border']} !important;
}}
[data-testid="stSidebar"] *:not([data-testid="stSidebarCollapseButton"] *):not([data-testid="stSidebarCollapsedControl"] *) {{
    color: {T['text']} !important;
    font-family: 'Syne', sans-serif !important;
}}
[data-testid="stSidebar"] label {{
    font-size: 0.72rem !important; font-weight: 700 !important;
    letter-spacing: 0.8px !important; text-transform: uppercase !important;
    color: {T['muted']} !important;
}}
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="input"] {{
    background: {T['bg3']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 8px !important;
}}
[data-testid="stMetric"] {{
    background: {T['bg2']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
}}
[data-testid="stMetricLabel"] p {{
    font-size: 0.68rem !important; font-weight: 700 !important;
    letter-spacing: 1px !important; text-transform: uppercase !important;
    color: {T['muted']} !important;
}}
[data-testid="stMetricValue"] {{
    font-family: 'Space Mono', monospace !important;
    font-size: 1.6rem !important; font-weight: 700 !important;
    color: {T['text']} !important;
}}
[data-testid="stTabs"] [role="tablist"] {{
    background: {T['bg2']} !important;
    border: 1px solid {T['border']} !important;
    border-bottom: none !important;
    border-radius: 12px 12px 0 0 !important;
    padding: 0 0.5rem !important;
    gap: 0 !important;
}}
button[role="tab"] {{
    font-family: 'Syne', sans-serif !important;
    font-size: 0.75rem !important; font-weight: 700 !important;
    letter-spacing: 0.6px !important; text-transform: uppercase !important;
    color: {T['muted']} !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important; padding: 0.75rem 1.1rem !important;
    background: transparent !important;
}}
button[role="tab"][aria-selected="true"] {{
    color: {T['accent']} !important;
    border-bottom: 2px solid {T['accent']} !important;
}}
[data-testid="stTabs"] [data-baseweb="tab-panel"] {{
    background: {T['bg2']} !important;
    border: 1px solid {T['border']} !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
    padding: 1.5rem !important;
}}
[data-testid="stDataFrame"] {{
    border: 1px solid {T['border']} !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}}
[data-testid="stDataFrame"] th {{
    background: {T['bg3']} !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.68rem !important; font-weight: 700 !important;
    text-transform: uppercase !important; letter-spacing: 0.8px !important;
    color: {T['muted']} !important;
}}
[data-testid="stDataFrame"] td {{
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
}}
[data-baseweb="input"] input, [data-baseweb="select"] div {{
    background: {T['bg3']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 8px !important;
    color: {T['text']} !important;
    font-family: 'Syne', sans-serif !important;
}}
[data-baseweb="tag"] {{
    background: {T['accent']}33 !important;
    border: 1px solid {T['accent']} !important;
    border-radius: 6px !important;
}}
.stButton > button {{
    background: {T['accent']} !important; color: #fff !important;
    border: none !important; border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; font-size: 0.8rem !important;
    padding: 0.45rem 1.1rem !important;
}}
.stButton > button:hover {{ opacity: 0.85 !important; }}
[data-testid="stAlert"] {{ border-radius: 10px !important; }}
hr {{ border-color: {T['border']} !important; margin: 1rem 0 !important; }}

/* ── Sidebar collapse button fix ── */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] {{
    color: white !important;
    font-size: 1 !important;
}}
[data-testid="collapsedControl"] svg,
[data-testid="stSidebarCollapsedControl"] svg {{
    display: block !important;
}}
button[kind="header"] span,
[data-testid="stSidebarNavCollapseIcon"] {{
    font-size: 0 !important;
    color: transparent !important;
}}
/* Target the Material icon text node directly */
[data-testid="stSidebar"] button > span[class*="material"] {{
    font-size: 0 !important;
}}
section[data-testid="stSidebar"] > div > div > div > button > div > span {{
    font-size: 0 !important;
    color: transparent !important;
}}
/* The collapse toggle button that shows "keyboard_double_arrow_left" */
button[data-testid="baseButton-header"] {{
    font-size: 0 !important;
    color: transparent !important;
}}
button[data-testid="baseButton-header"] span {{
    font-size: 1.2rem !important;
    color: {T['muted']} !important;
    font-family: 'Material Symbols Rounded', sans-serif !important;
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
CREATOR_COLORS = {
    "OpenAI": "#10b981", "Anthropic": "#7c6af7", "Google": "#22d3ee",
    "Meta": "#f59e0b", "DeepSeek": "#f472b6", "xAI": "#a78bfa",
    "Mistral": "#34d399", "Amazon": "#fb923c", "Alibaba": "#60a5fa",
    "NVIDIA": "#4ade80", "Cohere": "#e879f9", "Microsoft Azure": "#38bdf8",
}
CTX_ORDER = {
    "4k":1,"8k":2,"16k":3,"32k":4,"33k":5,"64k":6,"66k":7,
    "128k":8,"130k":9,"131k":10,"200k":11,"205k":12,"256k":13,
    "258k":14,"262k":15,"400k":16,"512k":17,"1m":18,"2m":19,"10m":20,
}
CTX_NUM = {
    "4k":4_000,"8k":8_000,"16k":16_000,"32k":32_000,"33k":33_000,
    "64k":64_000,"66k":66_000,"128k":128_000,"130k":130_000,"131k":131_000,
    "200k":200_000,"205k":205_000,"256k":256_000,"258k":258_000,"262k":262_000,
    "400k":400_000,"512k":512_000,"1m":1_000_000,"2m":2_000_000,"10m":10_000_000,
}

# ─────────────────────────────────────────────────────────────────────────────
#  DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("aimodels.csv")
    df.columns = df.columns.str.strip()
    df = df.rename(columns={
        "Price (Blended USD/1M Tokens)": "Price",
        "Speed(median token/s)":          "Speed",
        "Latency (First Answer Chunk /s)": "Latency",
        "Intelligence Index":              "Intelligence",
        "Context Window":                  "Context",
    })
    def to_num(series):
        return pd.to_numeric(
            series.astype(str).str.replace(r"[^\d.]", "", regex=True),
            errors="coerce",
        )
    df["Price"]        = to_num(df["Price"])
    df["Speed"]        = to_num(df["Speed"])
    df["Latency"]      = to_num(df["Latency"])
    df["Intelligence"] = to_num(df["Intelligence"])
    df["Context_Num"]  = df["Context"].str.lower().map(CTX_NUM)
    df["Color"]        = df["Creator"].map(CREATOR_COLORS).fillna("#6b7280")
    return df

df = load_data()

# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:0.8rem 0 0.2rem">
      <div style="font-family:'Space Mono',monospace;font-size:0.65rem;
                  color:{T['accent']};letter-spacing:2px;text-transform:uppercase">
        LLMRank 2026
      </div>
      <p style="font-size:0.72rem;color:{T['muted']};margin-top:0.3rem;line-height:1.5">
        Filter &amp; explore 188 models from 37 AI labs.
      </p>
    </div><hr>
    """, unsafe_allow_html=True)

    all_creators = sorted(df["Creator"].dropna().unique())
    sel_creators = st.multiselect("Filter by Lab", all_creators, placeholder="All labs")

    ctx_options = sorted(df["Context"].dropna().unique(),
                         key=lambda x: CTX_ORDER.get(x.lower(), 99))
    sel_ctx = st.multiselect("Context Window", ctx_options, placeholder="Any")

    max_p = float(df["Price"].max(skipna=True)) + 0.01
    budget = st.slider("Max Price ($/1M tokens)", 0.0, max_p, max_p, step=0.1, format="$%.2f")

    max_spd = int(df["Speed"].max(skipna=True))
    min_speed = st.slider("Min Speed (tok/s)", 0, max_spd, 0)

    output_tokens = st.slider("Output tokens (time estimate)", 50, 5000, 500, step=50)

    st.markdown(
        f"<hr><p style='font-size:0.65rem;color:{T['muted']}'>188 models · 37 labs · 2026</p>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
#  FILTER & DERIVED COLUMNS
# ─────────────────────────────────────────────────────────────────────────────
fdf = df.copy()
if sel_creators:
    fdf = fdf[fdf["Creator"].isin(sel_creators)]
if sel_ctx:
    fdf = fdf[fdf["Context"].isin(sel_ctx)]
fdf = fdf[fdf["Price"].fillna(0) <= budget]
fdf = fdf[fdf["Speed"].fillna(0) >= min_speed].copy()

def _est(row):
    s, la = row["Speed"], row["Latency"]
    if pd.notna(s) and s > 0 and pd.notna(la):
        return float(la) + output_tokens / float(s)
    return np.nan

fdf["Est_Time"] = fdf.apply(_est, axis=1)

score_src = fdf[fdf["Latency"].fillna(0) > 0].copy()
if not score_src.empty:
    score_src["_sc"] = (
        (1 / score_src["Latency"].clip(lower=0.01)) * 0.25
        + score_src["Speed"].fillna(0) * 0.30
        + score_src["Intelligence"].fillna(0) * 0.45
    )
    best = score_src.sort_values("_sc", ascending=False).iloc[0]
else:
    best = None

# ─────────────────────────────────────────────────────────────────────────────
#  UI HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def plotly_theme(fig, height=360):
    fig.update_layout(
        template=T["ptpl"], paper_bgcolor=T["paper"], plot_bgcolor=T["plot"],
        font=dict(family="Space Mono, monospace", color=T["text"], size=11),
        height=height, margin=dict(l=10, r=10, t=44, b=10),
        legend=dict(bgcolor=T["bg3"], bordercolor=T["border"],
                    borderwidth=1, font=dict(size=10)),
    )
    fig.update_xaxes(gridcolor=T["grid"], zerolinecolor=T["grid"])
    fig.update_yaxes(gridcolor=T["grid"], zerolinecolor=T["grid"])
    return fig

def divider():
    st.markdown(
        f"<div style='height:1px;background:{T['border']};margin:1.2rem 0'></div>",
        unsafe_allow_html=True,
    )

def accent_bar():
    st.markdown(
        f"<div style='height:3px;"
        f"background:linear-gradient(90deg,{T['accent']},{T['accent2']},{T['accent3']});"
        f"border-radius:2px;margin:0.8rem 0'></div>",
        unsafe_allow_html=True,
    )

def section_label(mono_txt, big_txt):
    st.markdown(f"""
    <div style="margin-bottom:1rem">
      <div style="font-family:'Space Mono',monospace;font-size:0.65rem;color:{T['accent2']};
                  letter-spacing:2px;text-transform:uppercase;margin-bottom:0.4rem">
        // {mono_txt}
      </div>
      <h2 style="font-family:'Syne',sans-serif;font-size:1.55rem;font-weight:800;
                 letter-spacing:-0.4px;color:{T['text']};margin:0;line-height:1.1">
        {big_txt}
      </h2>
    </div>""", unsafe_allow_html=True)

def stat_card_html(num, color, label):
    return (
        f"<div style='background:{T['bg3']};border:1px solid {T['border']};"
        f"border-radius:10px;padding:1rem 1.2rem;text-align:center'>"
        f"<div style='font-family:Space Mono,monospace;font-size:1.65rem;font-weight:700;"
        f"color:{color};line-height:1'>{num}</div>"
        f"<div style='font-size:0.63rem;color:{T['muted']};text-transform:uppercase;"
        f"letter-spacing:0.8px;margin-top:0.35rem'>{label}</div>"
        f"</div>"
    )

def insight_card_html(num, color, label, detail, items=None):
    rows = ""
    if items:
        rows = "<div style='margin-top:0.8rem'>" + "".join(
            f"<div style='display:flex;justify-content:space-between;padding:0.28rem 0;"
            f"border-bottom:1px solid {T['border']};font-size:0.76rem'>"
            f"<span style='color:{T['text']}'>{n}</span>"
            f"<span style='font-family:Space Mono,monospace;color:{T['muted']};font-size:0.72rem'>{v}</span>"
            f"</div>"
            for n, v in items
        ) + "</div>"
    return (
        f"<div style='background:{T['bg2']};border:1px solid {T['border']};"
        f"border-radius:12px;padding:1.3rem 1.4rem;margin-bottom:0'>"
        f"<div style='font-family:Space Mono,monospace;font-size:1.85rem;font-weight:700;"
        f"color:{color};line-height:1'>{num}</div>"
        f"<div style='font-size:0.63rem;color:{T['muted']};text-transform:uppercase;"
        f"letter-spacing:0.8px;margin-top:0.3rem'>{label}</div>"
        f"<div style='font-size:0.79rem;color:{T['text']};margin-top:0.7rem;line-height:1.6'>{detail}</div>"
        f"{rows}</div>"
    )

def price_bucket(p):
    if p == 0:   return "Free ($0)"
    if p < 0.5:  return "< $0.50"
    if p < 2:    return "$0.50–$2"
    if p < 5:    return "$2–$5"
    if p < 10:   return "$5–$10"
    return "> $10"

# ─────────────────────────────────────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="padding:1.4rem 0 0.6rem">
  <div style="font-family:'Space Mono',monospace;font-size:0.66rem;color:{T['accent2']};
              letter-spacing:2.5px;text-transform:uppercase;margin-bottom:0.5rem">
    // Best LLMs for Coding — 2026 Rankings
  </div>
  <h1 style="font-family:'Syne',sans-serif;font-size:2.5rem;font-weight:800;
             letter-spacing:-1.2px;color:{T['text']};margin:0;line-height:1.05">
    LLM<span style="color:{T['accent']}">Rank</span>
    <span style="color:{T['muted']};font-size:1.5rem;font-weight:600"> 2026</span>
  </h1>
  <p style="color:{T['muted']};font-size:0.87rem;margin-top:0.5rem;max-width:560px;line-height:1.6">
    Every major AI model ranked for coding — intelligence, speed, latency &amp; cost.
    <span style="color:{T['accent2']};font-family:'Space Mono',monospace;font-size:0.78rem">
      &nbsp;{len(fdf)} models shown</span> of 188.
  </p>
</div>
""", unsafe_allow_html=True)

accent_bar()

# ─────────────────────────────────────────────────────────────────────────────
#  KPI ROW
# ─────────────────────────────────────────────────────────────────────────────
k = st.columns(6)
kpis = [
    (str(len(fdf)),                                                                        T["accent"],  "Models"),
    (str(fdf["Creator"].nunique()),                                                        T["accent2"], "Labs"),
    (str(int(fdf["Intelligence"].max(skipna=True))) if fdf["Intelligence"].notna().any() else "—", T["gold"],   "Top Intel"),
    (str(int(fdf["Speed"].max(skipna=True))) if fdf["Speed"].notna().any() else "—",       T["accent3"], "Fastest t/s"),
    (str(int((fdf["Price"] == 0).sum())),                                                  T["green"],   "Free Models"),
    (f"${fdf.loc[fdf['Price']>0,'Price'].mean():.2f}" if (fdf["Price"]>0).any() else "—", T["muted"],   "Avg Price"),
]
for col, (val, color, label) in zip(k, kpis):
    with col:
        st.markdown(stat_card_html(val, color, label), unsafe_allow_html=True)

st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  RECOMMENDED MODEL BANNER
# ─────────────────────────────────────────────────────────────────────────────
if best is not None:
    et        = f"{best['Est_Time']:.2f}s" if pd.notna(best.get("Est_Time")) else "—"
    intel_v   = str(int(best["Intelligence"])) if pd.notna(best["Intelligence"]) else "—"
    speed_v   = str(int(best["Speed"])) + " t/s" if pd.notna(best["Speed"]) else "—"
    price_v   = f"${best['Price']:.2f}" if pd.notna(best["Price"]) else "—"
    ctx_v     = str(best["Context"])
    chips = [("Intelligence", intel_v, T["accent"]),
             ("Speed",        speed_v, T["accent2"]),
             ("Price / 1M",   price_v, T["accent3"]),
             ("Est. Time",    et,      T["gold"]),
             ("Context",      ctx_v,   T["green"])]
    chips_html = "".join(
        f"<div><div style='font-size:0.58rem;color:{T['muted']};text-transform:uppercase;"
        f"letter-spacing:0.8px;margin-bottom:0.2rem'>{lb}</div>"
        f"<div style='font-family:Space Mono,monospace;font-size:1rem;"
        f"font-weight:700;color:{cl}'>{v}</div></div>"
        for lb, v, cl in chips
    )
    st.markdown(f"""
    <div style="background:{T['bg2']};border:1px solid {T['border']};
                border-left:3px solid {T['accent']};border-radius:12px;
                padding:1.2rem 1.6rem;margin-bottom:0.4rem">
      <div style="display:flex;align-items:flex-start;gap:2rem;flex-wrap:wrap">
        <div>
          <div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:{T['accent2']};
                      letter-spacing:2px;text-transform:uppercase;margin-bottom:0.3rem">
            Recommended for your filters
          </div>
          <div style="font-size:1.2rem;font-weight:800;color:{T['text']};
                      letter-spacing:-0.3px">{best['Model']}</div>
          <div style="font-size:0.73rem;color:{T['muted']};margin-top:0.2rem">{best['Creator']}</div>
        </div>
        <div style="display:flex;gap:1.8rem;flex-wrap:wrap;align-items:center">
          {chips_html}
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

accent_bar()

# ─────────────────────────────────────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "  Leaderboard",
    "  Analytics",
    "  Compare",
    "  Insights",
])

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — LEADERBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    section_label("Rankings", "Model Leaderboard")

    c1, c2, c3 = st.columns([3, 1.2, 0.8])
    with c1:
        search = st.text_input("", placeholder="  Search models or labs…",
                               label_visibility="collapsed")
    with c2:
        sort_by = st.selectbox("", ["Intelligence ↓","Price ↑","Speed ↓","Latency ↑"],
                               label_visibility="collapsed")
    with c3:
        show_n = st.selectbox("", [25, 50, 100, 188], label_visibility="collapsed")

    disp = fdf.copy()
    if search:
        mask = (disp["Model"].str.contains(search, case=False, na=False) |
                disp["Creator"].str.contains(search, case=False, na=False))
        disp = disp[mask]

    s_col, s_asc = {"Intelligence ↓":("Intelligence",False),"Price ↑":("Price",True),
                    "Speed ↓":("Speed",False),"Latency ↑":("Latency",True)}[sort_by]
    disp = disp.sort_values(s_col, ascending=s_asc, na_position="last").reset_index(drop=True)
    disp.index = disp.index + 1

    ecol = f"Est Time ({output_tokens}t)"
    show = disp[["Model","Creator","Context","Intelligence","Price","Speed","Latency","Est_Time"]].head(show_n).copy()
    show = show.rename(columns={"Est_Time": ecol})

    st.dataframe(
        show.style.format({
            "Intelligence": lambda x: f"{int(x)}"     if pd.notna(x) else "—",
            "Price":        lambda x: "Free"           if x == 0 else (f"${x:.3f}" if pd.notna(x) else "—"),
            "Speed":        lambda x: f"{int(x)} t/s" if pd.notna(x) and x > 0 else "—",
            "Latency":      lambda x: f"{x:.2f}s"     if pd.notna(x) and x > 0 else "—",
            ecol:           lambda x: f"{x:.2f}s"     if pd.notna(x) else "—",
        })
        .background_gradient(subset=["Intelligence"], cmap="Purples", low=0.2)
        .background_gradient(subset=["Speed"],        cmap="Blues",   low=0.2)
        .bar(subset=["Price"], color=T["accent3"] + "55"),
        use_container_width=True,
        height=580,
    )
    st.markdown(
        f"<p style='font-size:0.72rem;color:{T['muted']};margin-top:0.4rem'>"
        f"Showing {min(show_n, len(disp))} of {len(disp)} models</p>",
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    section_label("Charts", "Model Analytics")

    top20 = fdf[fdf["Intelligence"].notna()].sort_values("Intelligence", ascending=False).head(20)
    if not top20.empty:
        cm = {c: top20.loc[top20["Creator"]==c,"Color"].iloc[0] for c in top20["Creator"].unique()}
        fig = px.bar(top20, x="Intelligence", y="Model", orientation="h",
                     color="Creator", color_discrete_map=cm,
                     title=" Top 20 Models — Intelligence Index",
                     hover_data={"Creator":True,"Context":True})
        fig.update_layout(yaxis={"categoryorder":"total ascending"}, showlegend=False)
        st.plotly_chart(plotly_theme(fig, 500), use_container_width=True)

    divider()
    ca, cb = st.columns(2)

    with ca:
        sdf = fdf[fdf["Intelligence"].notna() & fdf["Price"].notna()].copy()
        if not sdf.empty:
            cm2 = {c: sdf.loc[sdf["Creator"]==c,"Color"].iloc[0] for c in sdf["Creator"].unique()}
            fig2 = px.scatter(sdf, x="Price", y="Intelligence",
                              color="Creator", color_discrete_map=cm2,
                              hover_name="Model", size="Speed", size_max=22,
                              title=" Cost vs Intelligence (bubble = speed)",
                              labels={"Price":"Price $/1M tokens"})
            fig2.update_layout(showlegend=False)
            st.plotly_chart(plotly_theme(fig2), use_container_width=True)

    with cb:
        sldf = fdf[fdf["Speed"].fillna(0) > 0].copy()
        if not sldf.empty:
            cm3 = {c: sldf.loc[sldf["Creator"]==c,"Color"].iloc[0] for c in sldf["Creator"].unique()}
            fig3 = px.scatter(sldf, x="Speed", y="Latency",
                              color="Creator", color_discrete_map=cm3,
                              hover_name="Model", title=" Speed vs Latency",
                              labels={"Speed":"Speed (tok/s)","Latency":"Latency (s)"})
            fig3.update_layout(showlegend=False)
            st.plotly_chart(plotly_theme(fig3), use_container_width=True)

    divider()
    cc_col, cd = st.columns(2)

    with cc_col:
        cc = fdf["Creator"].value_counts().head(12).reset_index()
        cc.columns = ["Creator","Count"]
        cc["Color"] = cc["Creator"].map(CREATOR_COLORS).fillna("#6b7280")
        fig4 = px.bar(cc, x="Count", y="Creator", orientation="h",
                      color="Creator",
                      color_discrete_map=dict(zip(cc["Creator"], cc["Color"])),
                      title=" Models per Lab (Top 12)")
        fig4.update_layout(showlegend=False, yaxis={"categoryorder":"total ascending"})
        st.plotly_chart(plotly_theme(fig4), use_container_width=True)

    with cd:
        pdf = fdf[fdf["Price"].notna()].copy()
        pdf["Bucket"] = pdf["Price"].apply(price_bucket)
        bkt = pdf["Bucket"].value_counts().reset_index()
        bkt.columns = ["Bucket","Count"]
        fig5 = px.pie(bkt, values="Count", names="Bucket",
                      title=" Price Distribution",
                      color_discrete_sequence=[T["accent2"],"#4ade80",T["accent"],
                                               T["accent3"],T["gold"],"#f87171"],
                      hole=0.45)
        fig5.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(plotly_theme(fig5), use_container_width=True)

    divider()
    ctx_c = fdf["Context"].value_counts().reset_index()
    ctx_c.columns = ["Context","Count"]
    ctx_c["ord"] = ctx_c["Context"].str.lower().map(CTX_ORDER).fillna(99)
    ctx_c = ctx_c.sort_values("ord")
    fig6 = px.bar(ctx_c, x="Context", y="Count",
                  title=" Context Window Distribution",
                  color="Count",
                  color_continuous_scale=[[0, T["bg3"]], [1, T["accent"]]])
    fig6.update_layout(coloraxis_showscale=False)
    st.plotly_chart(plotly_theme(fig6, 290), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — COMPARE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    section_label("Head-to-Head", "Compare Models")
    st.markdown(
        f"<p style='font-size:0.82rem;color:{T['muted']};margin-bottom:1rem'>"
        "Select 2–4 models for a side-by-side breakdown.</p>",
        unsafe_allow_html=True,
    )

    all_models = sorted(fdf["Model"].dropna().unique())
    defaults = [m for m in ["GPT-5.2 (xhigh)","Claude Opus 4.5","Gemini 3 Pro Preview (high)"]
                if m in all_models][:3]
    selected = st.multiselect("Choose models", all_models, default=defaults, max_selections=4)

    if len(selected) < 2:
        st.info(" Select at least 2 models to compare.")
    else:
        model_lookup = {}
        for model_name in selected:
            matches = fdf[fdf["Model"] == model_name]
            if not matches.empty:
                model_lookup[model_name] = matches.iloc[0]

        def _is_na(v):
            if v is None:
                return True
            try:
                return bool(np.isnan(float(v)))
            except (TypeError, ValueError):
                return False

        def fmt_val(v, col):
            if _is_na(v):
                return "—"
            if col == "Intelligence":
                return str(int(float(v)))
            if col == "Price":
                return "Free" if float(v) == 0 else f"${float(v):.3f}"
            if col == "Speed":
                return f"{int(float(v))} t/s" if float(v) > 0 else "—"
            if col == "Latency":
                return f"{float(v):.2f}s" if float(v) > 0 else "—"
            if col == "Est_Time":
                return f"{float(v):.2f}s"
            return str(v)

        metric_defs = [
            ("Creator",      "Creator",           None),
            ("Context",      "Context Window",    None),
            ("Intelligence", "Intelligence Index", True),
            ("Price",        "Price / 1M tokens", False),
            ("Speed",        "Speed (tok/s)",      True),
            ("Latency",      "Latency (s)",        False),
            ("Est_Time",     f"Est Time ({output_tokens}t)", False),
        ]

        table_rows = []
        for col, label, higher_better in metric_defs:
            row = {"Metric": label}
            raw = {}
            for m in selected:
                if m in model_lookup and col in model_lookup[m].index:
                    raw[m] = model_lookup[m][col]
                else:
                    raw[m] = None

            best_key = None
            if higher_better is not None:
                num_vals = {}
                for m, v in raw.items():
                    if not _is_na(v):
                        try:
                            num_vals[m] = float(v)
                        except (TypeError, ValueError):
                            pass
                if num_vals:
                    best_key = (max if higher_better else min)(num_vals, key=num_vals.get)

            for m in selected:
                cell = fmt_val(raw[m], col)
                if m == best_key:
                    cell = " " + cell
                row[m] = cell

            table_rows.append(row)

        cmp_df = pd.DataFrame(table_rows).set_index("Metric")
        st.dataframe(cmp_df, use_container_width=True, height=310)

        divider()

        radar_cols = ["Intelligence","Speed","Latency","Price"]
        radar_vals = {}
        for m in selected:
            if m not in model_lookup:
                continue
            row_r = {}
            for col in radar_cols:
                v = model_lookup[m].get(col) if hasattr(model_lookup[m], "get") else model_lookup[m][col]
                try:
                    row_r[col] = float(v) if not _is_na(v) else np.nan
                except (TypeError, ValueError):
                    row_r[col] = np.nan
            radar_vals[m] = row_r

        radar_norm = {}
        for col in radar_cols:
            mx = df[col].max(skipna=True)
            pos = df.loc[df[col] > 0, col]
            mn = pos.min(skipna=True) if not pos.empty else 0.0
            span = float(mx - mn) + 1e-9
            for m in selected:
                if m not in radar_norm:
                    radar_norm[m] = {}
                v = radar_vals.get(m, {}).get(col, np.nan)
                if np.isnan(v):
                    norm = 0.0
                elif col in ("Latency","Price"):
                    norm = 1.0 - (v - mn) / span
                else:
                    norm = (v - mn) / span
                radar_norm[m][col] = float(np.clip(norm, 0, 1))

        PALETTE = [T["accent"], T["accent2"], T["accent3"], T["gold"]]
        fig_r = go.Figure()
        for i, m in enumerate(selected):
            if m not in radar_norm:
                continue
            vals = [radar_norm[m][c] for c in radar_cols] + [radar_norm[m][radar_cols[0]]]
            cats = radar_cols + [radar_cols[0]]
            fig_r.add_trace(go.Scatterpolar(
                r=vals, theta=cats, name=m, fill="toself", opacity=0.22,
                line=dict(color=PALETTE[i % 4], width=2.5),
                marker=dict(color=PALETTE[i % 4]),
            ))
        fig_r.update_layout(
            polar=dict(
                bgcolor=T["bg3"],
                radialaxis=dict(visible=True, range=[0,1], gridcolor=T["border"],
                                tickfont=dict(size=9, color=T["muted"])),
                angularaxis=dict(gridcolor=T["border"]),
            ),
            paper_bgcolor=T["paper"],
            font=dict(family="Space Mono, monospace", color=T["text"], size=11),
            legend=dict(bgcolor=T["bg3"], bordercolor=T["border"], borderwidth=1),
            title=dict(text="Normalised Radar — higher = better on all axes",
                       font=dict(size=11, color=T["muted"])),
            height=420, margin=dict(l=60, r=60, t=60, b=30),
        )
        st.plotly_chart(fig_r, use_container_width=True)

        divider()

        bar_rows = [{"Model": m, "Intelligence": model_lookup[m]["Intelligence"],
                     "Speed": model_lookup[m]["Speed"]}
                    for m in selected if m in model_lookup]
        bar_rows2 = [{"Model": m, "Price": model_lookup[m]["Price"],
                      "Latency": model_lookup[m]["Latency"]}
                     for m in selected if m in model_lookup]

        ce, cf = st.columns(2)
        with ce:
            if bar_rows:
                bdf1 = pd.DataFrame(bar_rows).melt(id_vars="Model", var_name="Metric", value_name="Value")
                fb1  = px.bar(bdf1, x="Model", y="Value", color="Metric", barmode="group",
                              title="Intelligence & Speed",
                              color_discrete_map={"Intelligence":T["accent"],"Speed":T["accent2"]})
                st.plotly_chart(plotly_theme(fb1, 320), use_container_width=True)
        with cf:
            if bar_rows2:
                bdf2 = pd.DataFrame(bar_rows2).melt(id_vars="Model", var_name="Metric", value_name="Value")
                fb2  = px.bar(bdf2, x="Model", y="Value", color="Metric", barmode="group",
                              title="Price & Latency — lower is better",
                              color_discrete_map={"Price":T["accent3"],"Latency":T["gold"]})
                st.plotly_chart(plotly_theme(fb2, 320), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 4 — INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    section_label("Key Findings", "Market Insights")

    has_intel = fdf[fdf["Intelligence"].notna()]
    free_df   = fdf[fdf["Price"] == 0]
    paid_df   = fdf[fdf["Price"].fillna(-1) > 0]
    has_speed = fdf[fdf["Speed"].fillna(0) > 0]
    has_lat   = fdf[fdf["Latency"].fillna(0) > 0]
    large_ctx = fdf[fdf["Context_Num"].fillna(0) >= 1_000_000]

    fastest5  = has_speed.sort_values("Speed",   ascending=False).head(5)
    low_lat5  = has_lat.sort_values("Latency").head(5)

    avg_intel = has_intel["Intelligence"].mean() if not has_intel.empty else 0
    avg_price = paid_df["Price"].mean() if not paid_df.empty else 0
    top_model = (fdf.loc[fdf["Intelligence"].idxmax(), "Model"]
                 if fdf["Intelligence"].notna().any() else "—")

    top_lab = (has_intel.groupby("Creator")["Intelligence"].max()
               .sort_values(ascending=False).head(8))

    r1 = st.columns(3)
    disp_name = (top_model[:22] + "…") if len(top_model) > 22 else top_model
    with r1[0]:
        st.markdown(insight_card_html(
            disp_name, T["accent"], "Top Performing Model",
            f"<b>{top_model}</b> leads with the highest Intelligence Index in the current filtered set.",
        ), unsafe_allow_html=True)
    with r1[1]:
        st.markdown(insight_card_html(
            str(len(free_df)), T["accent2"], "Free Models Available",
            f"{len(free_df)} models at $0 from Google, Meta, Alibaba &amp; more.",
            list(zip(free_df["Model"].head(5).tolist(), free_df["Creator"].head(5).tolist())),
        ), unsafe_allow_html=True)
    with r1[2]:
        st.markdown(insight_card_html(
            f"{avg_intel:.1f}", T["gold"], "Avg Intelligence Index",
            f"Across {len(has_intel)} ranked models. Avg paid price: ${avg_price:.2f}/1M tokens.",
        ), unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    r2 = st.columns(3)
    spd_num  = str(int(fastest5.iloc[0]["Speed"])) if not fastest5.empty else "—"
    spd_mod  = fastest5.iloc[0]["Model"]           if not fastest5.empty else "—"
    spd_lab  = fastest5.iloc[0]["Creator"]          if not fastest5.empty else "—"
    lat_num  = f"{low_lat5.iloc[0]['Latency']:.2f}s" if not low_lat5.empty else "—"
    lat_mod  = low_lat5.iloc[0]["Model"]              if not low_lat5.empty else "—"

    with r2[0]:
        st.markdown(insight_card_html(
            spd_num, T["accent3"], "Fastest Model (tok/s)",
            f"<b>{spd_mod}</b> by {spd_lab}.",
            [(r["Model"][:24], f"{int(r['Speed'])} t/s") for _, r in fastest5.iterrows()],
        ), unsafe_allow_html=True)
    with r2[1]:
        st.markdown(insight_card_html(
            lat_num, T["green"], "Lowest Latency",
            f"<b>{lat_mod}</b> achieves the fastest time-to-first-token.",
            [(r["Model"][:24], f"{r['Latency']:.2f}s") for _, r in low_lat5.iterrows()],
        ), unsafe_allow_html=True)
    with r2[2]:
        st.markdown(insight_card_html(
            str(len(large_ctx)), "#a78bfa", "Models with 1M+ Context",
            f"{len(large_ctx)} models offer 1M+ token context — ideal for full codebase analysis.",
            [(r["Model"][:24], r["Context"]) for _, r in large_ctx.head(5).iterrows()],
        ), unsafe_allow_html=True)

    divider()

    section_label("Lab Rankings", "Best Intelligence by Lab")
    if not top_lab.empty:
        tl = top_lab.reset_index()
        tl.columns = ["Creator","Intelligence"]
        tl["Color"] = tl["Creator"].map(CREATOR_COLORS).fillna("#6b7280")
        fig_lab = px.bar(tl, x="Creator", y="Intelligence", color="Creator",
                         color_discrete_map=dict(zip(tl["Creator"], tl["Color"])),
                         title="Peak Intelligence Index per Lab")
        fig_lab.update_layout(showlegend=False)
        st.plotly_chart(plotly_theme(fig_lab, 320), use_container_width=True)

    tier_df = fdf[fdf["Intelligence"].notna() & fdf["Price"].notna()].copy()
    tier_df["Tier"] = tier_df["Price"].apply(price_bucket)
    tier_stats = tier_df.groupby("Tier")["Intelligence"].mean().reset_index()
    tier_order = ["Free ($0)","< $0.50","$0.50–$2","$2–$5","$5–$10","> $10"]
    tier_stats["Tier"] = pd.Categorical(tier_stats["Tier"], categories=tier_order, ordered=True)
    tier_stats = tier_stats.sort_values("Tier")
    if not tier_stats.empty:
        fig_t = px.line(tier_stats, x="Tier", y="Intelligence", markers=True,
                        title=" Avg Intelligence by Price Tier",
                        color_discrete_sequence=[T["accent"]])
        fig_t.update_traces(line_width=2.5, marker_size=9, marker_color=T["accent2"])
        st.plotly_chart(plotly_theme(fig_t, 280), use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────────────────────────
accent_bar()
st.markdown(f"""
<div style="text-align:center;padding:0.3rem 0 1.5rem;
            font-family:'Space Mono',monospace;font-size:0.7rem;color:{T['muted']}">
  LLMRank 2026 &nbsp;·&nbsp; {len(df)} models &nbsp;·&nbsp;
  {df['Creator'].nunique()} labs &nbsp;·&nbsp; Streamlit + Plotly
</div>
""", unsafe_allow_html=True)