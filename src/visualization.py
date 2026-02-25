"""
Module 4 – Fitness Visualization Dashboard
Interactive Plotly charts: calorie balance, macro trends,
workout frequency, body stats and progress ring.
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import random


# ── colour palette ────────────────────────────────────────────
C = {
    "purple": "#a29bfe",
    "pink":   "#fd79a8",
    "yellow": "#fdcb6e",
    "green":  "#55efc4",
    "blue":   "#74b9ff",
    "red":    "#ff7675",
}
LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    margin=dict(l=20, r=20, t=40, b=20),
)


# ── demo data generator ───────────────────────────────────────
def _demo_week():
    today = datetime.now()
    days  = [(today - timedelta(days=i)).strftime("%a %d") for i in range(6, -1, -1)]
    cal_in  = [random.randint(1600, 2500) for _ in days]
    cal_out = [random.randint(200,  700)  for _ in days]
    weight  = [72 - i * 0.15 + random.uniform(-0.2, 0.2) for i in range(7)]
    steps   = [random.randint(4000, 12000) for _ in days]
    return days, cal_in, cal_out, weight, steps


# ── individual chart builders ─────────────────────────────────
def calorie_balance_chart(days, cal_in, cal_out, tdee):
    net    = [i - o for i, o in zip(cal_in, cal_out)]
    fig = go.Figure()
    fig.add_bar(name="Intake",  x=days, y=cal_in,  marker_color=C["pink"],   opacity=0.85)
    fig.add_bar(name="Burned",  x=days, y=cal_out, marker_color=C["purple"], opacity=0.85)
    fig.add_scatter(name="Net", x=days, y=net,
                    mode="lines+markers",
                    line=dict(color=C["yellow"], width=2.5),
                    marker=dict(size=8, color=C["yellow"]))
    if tdee:
        fig.add_hline(y=tdee, line_dash="dot", line_color=C["green"],
                      annotation_text=f"Target {tdee:.0f} kcal",
                      annotation_font_color=C["green"])
    fig.update_layout(**LAYOUT, barmode="group",
                      legend=dict(bgcolor="rgba(0,0,0,0)"),
                      title=dict(text="Calorie Balance (7-day)", font=dict(color="white")),
                      xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                      yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="kcal"))
    return fig


def weight_trend_chart(days, weights):
    fig = go.Figure()
    fig.add_scatter(
        x=days, y=weights,
        mode="lines+markers",
        line=dict(color=C["purple"], width=3),
        marker=dict(size=9, color=C["pink"], line=dict(color=C["purple"], width=2)),
        fill="tozeroy",
        fillcolor="rgba(162,155,254,0.08)",
    )
    fig.update_layout(**LAYOUT,
                      title=dict(text="Body Weight Trend (kg)", font=dict(color="white")),
                      xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                      yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="kg"))
    return fig


def macro_breakdown_chart(protein_g, carbs_g, fat_g):
    fig = go.Figure(go.Pie(
        labels=["Protein", "Carbs", "Fat"],
        values=[protein_g * 4, carbs_g * 4, fat_g * 9],
        hole=0.55,
        marker=dict(colors=[C["purple"], C["pink"], C["yellow"]],
                    line=dict(color="#0d0d1a", width=2)),
        textfont=dict(color="white"),
    ))
    fig.update_layout(**LAYOUT,
                      legend=dict(bgcolor="rgba(0,0,0,0)"),
                      title=dict(text="Today's Macro Breakdown", font=dict(color="white")),
                      height=300)
    return fig


def steps_bar_chart(days, steps):
    colors = [C["green"] if s >= 8000 else C["yellow"] if s >= 5000 else C["red"] for s in steps]
    fig = go.Figure(go.Bar(
        x=days, y=steps,
        marker_color=colors,
        text=steps, textposition="outside", textfont=dict(color="white"),
    ))
    fig.add_hline(y=8000, line_dash="dot", line_color=C["green"],
                  annotation_text="Goal: 8000", annotation_font_color=C["green"])
    fig.update_layout(**LAYOUT,
                      title=dict(text="Daily Steps", font=dict(color="white")),
                      xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                      yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="steps"))
    return fig


def progress_ring(current_cal, target_cal):
    pct = min(current_cal / max(target_cal, 1) * 100, 100)
    color = C["green"] if pct < 90 else C["yellow"] if pct < 110 else C["red"]
    fig = go.Figure(go.Pie(
        values=[pct, max(0, 100 - pct)],
        hole=0.72,
        marker=dict(colors=[color, "rgba(255,255,255,0.05)"],
                    line=dict(color="#0d0d1a", width=1)),
        showlegend=False,
        textinfo="none",
    ))
    fig.add_annotation(
        text=f"{pct:.0f}%<br><span style='font-size:12px'>of goal</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=22, color="white"),
    )
    fig.update_layout(**LAYOUT, height=220,
                      title=dict(text="Calorie Goal Progress", font=dict(color="white")))
    return fig


def workout_category_chart(workout_log):
    cats = {}
    for w in workout_log:
        for ex in w.get("exercises", []):
            cats[ex["category"]] = cats.get(ex["category"], 0) + 1
    if not cats:
        cats = {"Cardio": 3, "Strength": 5, "Core": 2, "Flexibility": 1}  # demo
    colors_map = {"Cardio": C["red"], "Strength": C["purple"],
                  "Core": C["yellow"], "Flexibility": C["green"]}
    fig = go.Figure(go.Bar(
        x=list(cats.keys()), y=list(cats.values()),
        marker_color=[colors_map.get(k, C["blue"]) for k in cats],
        text=list(cats.values()), textposition="outside", textfont=dict(color="white"),
    ))
    fig.update_layout(**LAYOUT,
                      title=dict(text="Workout Categories Distribution", font=dict(color="white")),
                      xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                      yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="sessions"))
    return fig


# ── main renderer ─────────────────────────────────────────────
def render_visualization_dashboard():
    st.markdown('<h2 class="grad-text">📊 Fitness Visualization Dashboard</h2>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#7777aa;">Interactive charts tracking calories, macros, weight trends and workout patterns.</p>',
        unsafe_allow_html=True,
    )

    profile = st.session_state.user_profile
    food_log    = st.session_state.food_log
    workout_log = st.session_state.workout_log
    tdee        = profile.get("tdee", 2000)

    # ── today summary ─────────────────────────────────────
    today_cal_in  = sum(item.get("calories", 0) for item in food_log)
    today_cal_out = sum(w.get("calories_burned", 0) for w in workout_log)
    today_protein = sum(item.get("protein", 0) for item in food_log)
    today_carbs   = sum(item.get("carbs",   0) for item in food_log)
    today_fat     = sum(item.get("fat",     0) for item in food_log)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Today's Intake",   f"{today_cal_in:.0f} kcal")
    c2.metric("Today's Burned",   f"{today_cal_out:.0f} kcal")
    c3.metric("Net Calories",     f"{today_cal_in - today_cal_out:+.0f} kcal")
    c4.metric("TDEE Target",      f"{tdee:.0f} kcal")

    st.markdown("---")

    # ── demo / real flag ──────────────────────────────────
    use_demo = not food_log and not workout_log
    if use_demo:
        st.markdown(
            '<div class="warning-box">⚠️ No data logged yet — showing <b>demo charts</b>. '
            'Log meals & workouts to see your real data!</div>',
            unsafe_allow_html=True,
        )
    days, cal_in, cal_out, weights, steps = _demo_week()

    # ── row 1 ─────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(calorie_balance_chart(days, cal_in, cal_out, tdee), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(weight_trend_chart(days, weights), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── row 2 ─────────────────────────────────────────────
    col3, col4, col5 = st.columns([1, 1.5, 1])
    with col3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(progress_ring(today_cal_in, tdee), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        p = today_protein if today_protein else profile.get("macros", {}).get("protein", 150)
        c = today_carbs   if today_carbs   else profile.get("macros", {}).get("carbs",   200)
        f = today_fat     if today_fat     else profile.get("macros", {}).get("fat",     65)
        st.plotly_chart(macro_breakdown_chart(p, c, f), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(steps_bar_chart(days[-3:], steps[-3:]), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── row 3 ─────────────────────────────────────────────
    col6, col7 = st.columns(2)
    with col6:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(workout_category_chart(workout_log), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col7:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(steps_bar_chart(days, steps), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── weekly summary table ───────────────────────────────
    st.markdown("### 📅 Weekly Summary")
    summary_df = pd.DataFrame({
        "Day":       days,
        "Cal In":    [f"{v} kcal" for v in cal_in],
        "Cal Burned":[f"{v} kcal" for v in cal_out],
        "Net":       [f"{i-o:+d} kcal" for i, o in zip(cal_in, cal_out)],
        "Steps":     steps,
    })
    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True,
    )
