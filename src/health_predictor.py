"""
Module 3 – Health & Calorie Predictor
Computes BMI, BMR (Mifflin-St Jeor), TDEE, macro targets
and stores a user profile in session state.
"""
import streamlit as st
import plotly.graph_objects as go


# ── calculation helpers ───────────────────────────────────────
def calc_bmi(weight_kg: float, height_cm: float) -> float:
    h_m = height_cm / 100
    return round(weight_kg / (h_m ** 2), 1)

def bmi_category(bmi: float) -> tuple:
    if   bmi < 18.5: return "Underweight", "tag-blue"
    elif bmi < 25.0: return "Normal",       "tag-green"
    elif bmi < 30.0: return "Overweight",   "tag-orange"
    else:             return "Obese",        "tag-red"

def calc_bmr(weight_kg, height_cm, age, gender) -> float:
    """Mifflin-St Jeor equation."""
    if gender == "Male":
        return round(10 * weight_kg + 6.25 * height_cm - 5 * age + 5,   1)
    else:
        return round(10 * weight_kg + 6.25 * height_cm - 5 * age - 161, 1)

ACTIVITY_FACTORS = {
    "Sedentary (desk job, no exercise)":        1.2,
    "Lightly active (1-3 days/week)":           1.375,
    "Moderately active (3-5 days/week)":        1.55,
    "Very active (6-7 days/week)":              1.725,
    "Extremely active (athlete / 2x/day)":      1.9,
}
GOAL_ADJUSTMENTS = {
    "Lose Weight (aggressive −500 kcal)":   -500,
    "Lose Weight (moderate −250 kcal)":     -250,
    "Maintain Weight":                          0,
    "Gain Muscle (moderate +250 kcal)":     +250,
    "Bulk (aggressive +500 kcal)":          +500,
}

def calc_macros(tdee: float, goal: str) -> dict:
    """Return macro grams based on goal."""
    if "Lose" in goal:
        p_pct, c_pct, f_pct = 0.40, 0.35, 0.25
    elif "Bulk" in goal or "Gain" in goal:
        p_pct, c_pct, f_pct = 0.30, 0.45, 0.25
    else:
        p_pct, c_pct, f_pct = 0.30, 0.40, 0.30

    return {
        "protein": round(tdee * p_pct / 4, 1),  # 4 kcal/g
        "carbs":   round(tdee * c_pct / 4, 1),
        "fat":     round(tdee * f_pct / 9, 1),  # 9 kcal/g
    }


# ── chart helpers ─────────────────────────────────────────────
def bmi_gauge(bmi: float):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bmi,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "BMI", "font": {"color": "white", "size": 18}},
        number={"font": {"color": "#a29bfe", "size": 36}},
        gauge={
            "axis":  {"range": [10, 40], "tickcolor": "white"},
            "bar":   {"color": "#a29bfe"},
            "bgcolor": "rgba(0,0,0,0)",
            "steps": [
                {"range": [10,  18.5], "color": "rgba(116,185,255,0.25)"},
                {"range": [18.5,25.0], "color": "rgba(0,184,148,0.25)"},
                {"range": [25.0,30.0], "color": "rgba(253,203,110,0.25)"},
                {"range": [30.0,40.0], "color": "rgba(255,118,117,0.25)"},
            ],
            "threshold": {"line": {"color": "#fd79a8", "width": 3}, "value": bmi},
        },
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"},
        margin=dict(l=20, r=20, t=40, b=10),
        height=260,
    )
    return fig


def macro_donut(macros: dict, tdee: float):
    # guard for zero values
    v_prot  = macros["protein"] * 4
    v_carbs = macros["carbs"]   * 4
    v_fat   = macros["fat"]     * 9
    if v_prot + v_carbs + v_fat == 0:
        v_prot, v_carbs, v_fat = 1, 1, 1

    fig = go.Figure(go.Pie(
        labels=["Protein", "Carbs", "Fat"],
        values=[v_prot, v_carbs, v_fat],
        hole=0.60,
        marker=dict(
            colors=["#a29bfe", "#fd79a8", "#fdcb6e"],
            line=dict(color="#0d0d1a", width=2),
        ),
        textfont=dict(color="white"),
    ))
    fig.add_annotation(
        text=f"{tdee:.0f}<br>kcal",
        font={"size": 18, "color": "white"},
        showarrow=False,
        x=0.5, y=0.5
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="white"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=20, b=10),
        height=280,
    )
    return fig


# ── main renderer ─────────────────────────────────────────────
def render_health_predictor():
    st.markdown('<h2 class="grad-text">🔥 Health & Calorie Predictor</h2>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#7777aa;">Fill in your details to get BMI, BMR, TDEE '
        'and a personalised macro plan for your goal.</p>',
        unsafe_allow_html=True,
    )

    with st.form("health_form"):
        st.markdown("### 👤 Personal Details")
        c1, c2 = st.columns(2)
        with c1:
            name   = st.text_input("Your Name", value=st.session_state.user_profile.get("name", ""))
            age    = st.number_input("Age (years)", 10, 100, int(st.session_state.user_profile.get("age", 25)))
            gender = st.selectbox("Gender", ["Male", "Female"],
                                  index=0 if st.session_state.user_profile.get("gender","Male")=="Male" else 1)
        with c2:
            weight = st.number_input("Weight (kg)", 30.0, 200.0,
                                     float(st.session_state.user_profile.get("weight", 70.0)), 0.5)
            height = st.number_input("Height (cm)", 100.0, 250.0,
                                     float(st.session_state.user_profile.get("height", 170.0)), 0.5)

        st.markdown("### 🏃 Activity & Goal")
        c3, c4 = st.columns(2)
        with c3:
            activity = st.selectbox("Activity Level", list(ACTIVITY_FACTORS.keys()),
                                    index=list(ACTIVITY_FACTORS.keys()).index(
                                        st.session_state.user_profile.get("activity",
                                        "Moderately active (3-5 days/week)")
                                    ) if st.session_state.user_profile.get("activity") else 2)
        with c4:
            goal = st.selectbox("Fitness Goal", list(GOAL_ADJUSTMENTS.keys()),
                                index=list(GOAL_ADJUSTMENTS.keys()).index(
                                    st.session_state.user_profile.get("goal","Maintain Weight")
                                ) if st.session_state.user_profile.get("goal") else 2)

        submitted = st.form_submit_button("🔥 Calculate My Plan", use_container_width=True)

    if submitted or st.session_state.user_profile:
        # prefer fresh values if form was just submitted
        if submitted:
            w, h, a, g = weight, height, activity, goal
        else:
            p = st.session_state.user_profile
            w = p.get("weight", 70)
            h = p.get("height", 170)
            a = p.get("activity", "Moderately active (3-5 days/week)")
            g = p.get("goal", "Maintain Weight")
            age    = p.get("age", 25)
            gender = p.get("gender", "Male")
            name   = p.get("name", "User")

        bmi   = calc_bmi(w, h)
        bmr   = calc_bmr(w, h, age, gender)
        tdee  = round(bmr * ACTIVITY_FACTORS[a] + GOAL_ADJUSTMENTS[g])
        macros = calc_macros(tdee, g)
        bmi_cat, bmi_tag = bmi_category(bmi)

        # save to session state
        if submitted:
            st.session_state.user_profile = {
                "name": name, "age": age, "gender": gender,
                "weight": w, "height": h,
                "activity": a, "goal": g,
                "bmi": bmi, "bmr": bmr, "tdee": tdee,
                "macros": macros,
            }
            st.success(f"✅ Profile saved for {name}!")

        st.markdown("---")
        st.markdown("### 📊 Your Health Metrics")

        # ── top KPIs ──────────────────────────────────────
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("BMI",          bmi)
        c2.metric("BMR (base)",   f"{bmr:.0f} kcal")
        c3.metric("TDEE (target)",f"{tdee:.0f} kcal")
        c4.metric("Body Weight",  f"{w} kg")

        st.markdown(
            f'<span class="tag {bmi_tag}">BMI Category: {bmi_cat}</span>',
            unsafe_allow_html=True,
        )

        # ── charts ────────────────────────────────────────
        col_g, col_m = st.columns(2)
        with col_g:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("**BMI Gauge**")
            st.plotly_chart(bmi_gauge(bmi), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_m:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("**Daily Macro Split**")
            st.plotly_chart(macro_donut(macros, tdee), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # ── macro detail ─────────────────────────────────
        st.markdown("### 🥗 Daily Macro Targets")
        mc1, mc2, mc3 = st.columns(3)
        for col, key, unit, color, em in [
            (mc1, "protein", "g / day", "#a29bfe", "💪"),
            (mc2, "carbs",   "g / day", "#fd79a8", "🌾"),
            (mc3, "fat",     "g / day", "#fdcb6e", "🥑"),
        ]:
            with col:
                st.markdown(
                    f'<div class="metric-badge">'
                    f'<div style="font-size:1.6rem">{em}</div>'
                    f'<div class="val" style="color:{color}">{macros[key]}g</div>'
                    f'<div class="lbl">{key.title()} {unit}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        # ── tips ─────────────────────────────────────────
        st.markdown("### 💡 Personalised Tips")
        tips = []
        if bmi < 18.5:
            tips.append("🔵 You're underweight — focus on a caloric surplus with nutrient-dense foods.")
        elif bmi > 25:
            tips.append("🟡 Consider a moderate calorie deficit and prioritise whole foods.")

        water = round(w * 0.033, 1)
        tips += [
            f"💧 Drink at least **{water} L of water** per day (based on your weight).",
            f"🛌 Aim for **7-9 hours of sleep** to optimise recovery and hormone balance.",
            "🥦 Fill half your plate with vegetables at every meal.",
            f"🏃 Your activity level suggests **{'at least 30 min of moderate exercise daily' if 'Sedentary' in a else '60+ min of exercise daily'}**.",
        ]
        if "Lose" in g:
            tips.append("📉 Track your meals daily — consistency beats perfection in weight loss.")
        elif "Bulk" in g or "Gain" in g:
            tips.append("📈 Prioritise progressive overload in training to maximise muscle gain.")

        for t in tips:
            st.markdown(f'<div class="info-box">{t}</div>', unsafe_allow_html=True)
