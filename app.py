"""
╔══════════════════════════════════════════════════════════════╗
║        FitAI Pro - Multi-Modal Smart Fitness Planner         ║
║   Meal Detection • Workout NLP • Calorie AI • Dashboard      ║
╚══════════════════════════════════════════════════════════════╝
"""
import streamlit as st
import sys
from pathlib import Path

# ── path setup ────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent / "src"))

# ── page config (must be FIRST streamlit call) ────────────────
st.set_page_config(
    page_title="FitAI Pro – Smart Fitness Planner",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── global CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

.stApp {
    background: linear-gradient(135deg, #0d0d1a 0%, #1a1a3e 50%, #0d0d1a 100%);
    color: #e8e8ff;
}

/* sidebar */
[data-testid="stSidebar"] {
    background: rgba(15,15,40,0.95) !important;
    border-right: 1px solid rgba(162,155,254,0.2);
}
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.04) !important;
    color: #c5c3f0 !important;
    border: 1px solid rgba(162,155,254,0.15) !important;
    border-radius: 12px !important;
    width: 100% !important;
    text-align: left !important;
    padding: 0.7rem 1rem !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    transition: all 0.25s ease !important;
    margin-bottom: 4px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg,rgba(102,126,234,0.3),rgba(118,75,162,0.3)) !important;
    border-color: rgba(162,155,254,0.5) !important;
    color: #fff !important;
    transform: translateX(4px) !important;
}

/* cards */
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 1.8rem;
    margin: 0.8rem 0;
    backdrop-filter: blur(12px);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.glass-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(102,126,234,0.2);
}

/* gradient text */
.grad-text {
    background: linear-gradient(135deg,#a29bfe,#fd79a8,#fdcb6e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* hero title */
.hero-title {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg,#a29bfe 0%,#fd79a8 50%,#fdcb6e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}

/* metric badge */
.metric-badge {
    background: linear-gradient(135deg,rgba(102,126,234,0.2),rgba(118,75,162,0.2));
    border: 1px solid rgba(162,155,254,0.3);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
}
.metric-badge .val { font-size:1.8rem; font-weight:800; color:#a29bfe; }
.metric-badge .lbl { font-size:0.8rem; color:#8888aa; margin-top:2px; }

/* tag pills */
.tag {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.77rem;
    font-weight: 600;
    margin: 0.15rem;
}
.tag-green  { background:rgba(0,184,148,0.15);  color:#00d2a0; border:1px solid rgba(0,184,148,0.4); }
.tag-orange { background:rgba(253,203,110,0.15); color:#fdcb6e; border:1px solid rgba(253,203,110,0.4); }
.tag-red    { background:rgba(255,118,117,0.15); color:#ff7675; border:1px solid rgba(255,118,117,0.4); }
.tag-blue   { background:rgba(116,185,255,0.15); color:#74b9ff; border:1px solid rgba(116,185,255,0.4); }
.tag-purple { background:rgba(162,155,254,0.15); color:#a29bfe; border:1px solid rgba(162,155,254,0.4); }

/* primary button */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg,#667eea,#764ba2) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1.8rem !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102,126,234,0.45) !important;
}

/* info boxes */
.info-box {
    background: rgba(116,185,255,0.08);
    border-left: 4px solid #74b9ff;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    color: #c8deff;
}
.success-box {
    background: rgba(0,184,148,0.08);
    border-left: 4px solid #00d2a0;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    color: #b2f0df;
}
.warning-box {
    background: rgba(253,203,110,0.08);
    border-left: 4px solid #fdcb6e;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    color: #fff3c4;
}
.danger-box {
    background: rgba(255,118,117,0.08);
    border-left: 4px solid #ff7675;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.8rem 0;
    color: #ffd0cf;
}

/* tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255,255,255,0.03);
    border-radius: 14px;
    padding: 6px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    color: #9999bb !important;
    background: transparent !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#667eea,#764ba2) !important;
    color: #fff !important;
}

/* inputs */
.stTextInput input, .stTextArea textarea, .stNumberInput input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(162,155,254,0.2) !important;
    border-radius: 10px !important;
    color: #e8e8ff !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(162,155,254,0.2) !important;
    border-radius: 10px !important;
    color: #e8e8ff !important;
}
.stSlider [data-baseweb="slider"] { color: #a29bfe; }
[data-testid="stMetricValue"] { color: #a29bfe; font-weight: 800; }

/* logo area */
.sidebar-logo { text-align:center; font-size:3.5rem; margin:1rem 0 0.2rem; }
.sidebar-brand {
    text-align:center; font-size:1.4rem; font-weight:900;
    background:linear-gradient(135deg,#a29bfe,#fd79a8);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    margin-bottom:0.3rem;
}
.sidebar-sub { text-align:center; font-size:0.75rem; color:#6666aa; margin-bottom:1rem; }

/* divider */
hr { border-color: rgba(162,155,254,0.15) !important; }
</style>
""", unsafe_allow_html=True)

# ── lazy imports (after CSS) ──────────────────────────────────
from meal_detector    import render_meal_detector
from workout_analyzer import render_workout_analyzer
from health_predictor import render_health_predictor
from visualization    import render_visualization_dashboard
from user_planner     import render_user_planner

# ── session state bootstrap ───────────────────────────────────
for key, default in [
    ("food_log",      []),
    ("workout_log",   []),
    ("user_profile",  {}),
    ("current_page",  "home"),
    ("weekly_plan",   {}),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ── home page ─────────────────────────────────────────────────
def render_home():
    st.markdown('<div class="hero-title">💪 FitAI Pro</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#9999cc;font-size:1.1rem;margin-bottom:2rem;">'
        'Your Multi-Modal AI Fitness Companion — Meal Vision · Workout NLP · Smart Planning</p>',
        unsafe_allow_html=True,
    )

    # stats row
    total_cal_in  = sum(item.get("calories", 0) for item in st.session_state.food_log)
    total_cal_out = sum(item.get("calories_burned", 0) for item in st.session_state.workout_log)
    balance       = total_cal_in - total_cal_out
    tdee          = st.session_state.user_profile.get("tdee", 0)

    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl in [
        (c1, f"{total_cal_in:.0f}", "Calories In 🍽️"),
        (c2, f"{total_cal_out:.0f}", "Calories Burned 🔥"),
        (c3, f"{balance:+.0f}",     "Net Balance ⚖️"),
        (c4, f"{tdee:.0f}",         "Daily Target 🎯"),
    ]:
        with col:
            st.markdown(
                f'<div class="metric-badge"><div class="val">{val}</div>'
                f'<div class="lbl">{lbl}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # module cards
    modules = [
        ("🍽️", "Meal Image Detector",    "Upload a meal photo — AI detects food and instantly calculates macros & calories using image analysis.",    "meal"),
        ("🏋️", "NLP Workout Analyzer",   "Type your workout in plain English. NLP extracts exercises, sets, reps and estimates calories burned.",       "workout"),
        ("🔥", "Health & Calorie AI",    "Enter your body metrics. Get BMI, BMR, TDEE and a personalised macro breakdown for your fitness goal.",       "health"),
        ("📊", "Fitness Dashboard",      "Beautiful interactive charts tracking calorie balance, macro trends and weekly progress over time.",           "dashboard"),
        ("📅", "Smart Planner",          "Auto-generate personalised weekly meal & workout plans aligned with your calorie targets and fitness goals.", "planner"),
    ]

    row1 = st.columns(3)
    row2 = st.columns(2)
    for idx, (em, title, desc, page) in enumerate(modules):
        col = row1[idx] if idx < 3 else row2[idx - 3]
        with col:
            st.markdown(
                f'<div class="glass-card" style="min-height:200px">'
                f'<div style="font-size:2.4rem;margin-bottom:0.6rem">{em}</div>'
                f'<h4 style="color:#e8e8ff;margin-bottom:0.5rem">{title}</h4>'
                f'<p style="color:#7777aa;font-size:0.88rem;line-height:1.5">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if st.button(f"Open {title.split()[0]}", key=f"home_{page}", use_container_width=True):
                st.session_state.current_page = page
                st.rerun()

    # quick tip
    if not st.session_state.user_profile:
        st.markdown(
            '<div class="info-box">💡 <b>Get started:</b> Head to <b>Health & Calorie AI</b> to set up your profile first — '
            'it unlocks personalised calorie targets across all modules!</div>',
            unsafe_allow_html=True,
        )


# ── sidebar ───────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">💪</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-brand">FitAI Pro</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-sub">Multi-Modal Fitness Intelligence</div>', unsafe_allow_html=True)
        st.markdown("---")

        nav = {
            "🏠  Home":              "home",
            "🍽️  Meal Detector":     "meal",
            "🏋️  Workout Analyzer":  "workout",
            "🔥  Health Predictor":  "health",
            "📊  Dashboard":         "dashboard",
            "📅  Smart Planner":     "planner",
        }
        for label, key in nav.items():
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.current_page = key
                st.rerun()

        st.markdown("---")

        # mini profile
        p = st.session_state.user_profile
        if p:
            st.markdown("### 👤 Profile")
            st.markdown(
                f"**{p.get('name','User')}**  \n"
                f"Goal: `{p.get('goal','—')}`  \n"
                f"Target: `{p.get('tdee',0):.0f} kcal/day`"
            )
        else:
            st.markdown(
                '<div style="font-size:0.8rem;color:#6666aa;padding:0.5rem;">'
                'Set up your profile in <b>Health Predictor</b> for personalised insights.</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        # quick log counts
        st.markdown(
            f'<div style="font-size:0.8rem;color:#6666aa;">'
            f'📝 {len(st.session_state.food_log)} meals logged &nbsp;|&nbsp; '
            f'🏃 {len(st.session_state.workout_log)} workouts logged</div>',
            unsafe_allow_html=True,
        )


# ── main ──────────────────────────────────────────────────────
def main():
    render_sidebar()

    page = st.session_state.current_page
    dispatch = {
        "home":      render_home,
        "meal":      render_meal_detector,
        "workout":   render_workout_analyzer,
        "health":    render_health_predictor,
        "dashboard": render_visualization_dashboard,
        "planner":   render_user_planner,
    }
    dispatch.get(page, render_home)()


if __name__ == "__main__":
    main()
