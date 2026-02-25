"""
Module 2 - NLP Workout Analyzer
Parses free-text workout logs using regex & keyword NLP.
Extracts exercises, sets, reps, duration and estimates calories burned.
"""
import re
import json
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

# ── data ──────────────────────────────────────────────────────
_EX_PATH = Path(__file__).parent.parent / "data" / "exercises.json"


@st.cache_data
def load_exercise_db():
    with open(_EX_PATH, encoding="utf-8") as f:
        return json.load(f)


# ── NLP parsing helpers ───────────────────────────────────────
_WORD_NUMS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "fifteen": 15, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
}


def _replace_word_numbers(text):
    """Replace English number words with digits."""
    for word, num in _WORD_NUMS.items():
        text = re.sub(r"\b" + word + r"\b", str(num), text)
    return text


def _first_int(text, fallback=0):
    """Extract the first integer from text."""
    nums = re.findall(r"\d+", text)
    return int(nums[0]) if nums else fallback


def _first_float(text, fallback=0.0):
    """Extract the first float from text."""
    nums = re.findall(r"\d+\.?\d*", text)
    return float(nums[0]) if nums else fallback


def parse_workout_text(text, db):
    """
    Parse free-text workout log and return list of exercise dicts.
    Handles patterns like:
      - '3 sets x 10 pushups'
      - '3 sets of 10 pushups'
      - 'ran 5km in 30 minutes'
      - 'cycling 45 minutes'
      - '100 jumping jacks'
    """
    text = _replace_word_numbers(text.lower())
    results = []

    # Split on commas, semicolons, newlines, and periods followed by space
    chunks = re.split(r"[,\n;]|(?<=[a-z])\.\s+(?=[a-z0-9])", text)

    for raw_chunk in chunks:
        chunk = raw_chunk.strip()
        if len(chunk) < 3:
            continue

        # Find matching exercise from database
        matched_key = None
        matched_data = None
        for ex_key, ex_data in db.items():
            for kw in ex_data["keywords"]:
                if kw in chunk:
                    matched_key = ex_key
                    matched_data = ex_data
                    break
            if matched_key:
                break

        if not matched_key:
            continue

        # ── extract sets ──────────────────────────────────────
        # Patterns: "3 sets", "3x", "3 set"
        sets = 3  # default
        sets_match = re.search(r"(\d+)\s*(?:sets?|x\b)", chunk)
        if sets_match:
            sets = int(sets_match.group(1))

        # ── extract reps ──────────────────────────────────────
        # Patterns: "x 10", "x10", "10 reps", "10 repetitions", "× 10"
        reps = 10  # default
        reps_patterns = [
            r"(?:x|x\s*|×\s*)(\d+)\s*(?:reps?|repetitions?)?",
            r"(\d+)\s*(?:reps?|repetitions?)",
        ]
        for pattern in reps_patterns:
            m = re.search(pattern, chunk)
            if m:
                reps = int(m.group(1))
                break

        # ── extract duration (minutes) ────────────────────────
        # Patterns: "30 minutes", "30 min", "30mins"
        duration_min = None
        dur_match = re.search(r"(\d+\.?\d*)\s*(?:minutes?|mins?)", chunk)
        if dur_match:
            duration_min = float(dur_match.group(1))

        # If no explicit duration, estimate from sets × reps
        if duration_min is None:
            if matched_data["category"] == "Cardio":
                duration_min = 20.0  # default cardio session
            else:
                # ~3 seconds per rep + 90s rest between sets
                duration_min = round((sets * reps * 3) / 60 + (sets - 1) * 1.5, 1)
                duration_min = max(duration_min, 2.0)

        # ── extract distance ──────────────────────────────────
        distance_km = 0.0
        dist_match = re.search(r"(\d+\.?\d*)\s*(?:km|kilometers?|miles?|mi\b)", chunk)
        if dist_match:
            distance_km = float(dist_match.group(1))
            unit = chunk[dist_match.end():dist_match.end() + 5]
            if "mile" in unit or " mi" in unit:
                distance_km *= 1.609

        results.append({
            "exercise":    matched_key.title(),
            "category":    matched_data["category"],
            "muscle":      matched_data["muscle_group"],
            "emoji":       matched_data.get("emoji", ""),
            "sets":        sets,
            "reps":        reps,
            "duration":    round(float(duration_min), 1),
            "distance_km": round(distance_km, 2),
            "met":         float(matched_data["met"]),
        })

    return results


def calc_calories_burned(exercises, weight_kg):
    """MET * weight(kg) * time(hours)."""
    total = 0.0
    for ex in exercises:
        total += ex["met"] * weight_kg * (ex["duration"] / 60.0)
    return round(total, 1)


# ── chart ─────────────────────────────────────────────────────
def make_workout_bar(exercises, weight_kg):
    cat_colors = {
        "Cardio":      "#fd79a8",
        "Strength":    "#a29bfe",
        "Core":        "#fdcb6e",
        "Flexibility": "#55efc4",
    }
    names      = [ex["exercise"] for ex in exercises]
    cals       = [round(ex["met"] * weight_kg * ex["duration"] / 60.0, 1) for ex in exercises]
    bar_colors = [cat_colors.get(ex["category"], "#74b9ff") for ex in exercises]

    fig = go.Figure(go.Bar(
        x=names,
        y=cals,
        marker=dict(color=bar_colors, line=dict(color="#0d0d1a", width=1)),
        text=[f"{c} kcal" for c in cals],
        textposition="outside",
        textfont=dict(color="white", size=11),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(color="white", gridcolor="rgba(255,255,255,0.05)", tickangle=-20),
        yaxis=dict(color="white", gridcolor="rgba(255,255,255,0.05)", title="kcal"),
        font=dict(color="white"),
        margin=dict(l=10, r=10, t=40, b=40),
        height=320,
        title=dict(text="Calories Burned per Exercise", font=dict(color="white", size=14)),
    )
    return fig


def make_category_pie(exercises):
    """Pie chart of exercise category breakdown."""
    cats = {}
    for ex in exercises:
        cats[ex["category"]] = cats.get(ex["category"], 0) + ex["duration"]

    cat_colors = {
        "Cardio": "#fd79a8", "Strength": "#a29bfe",
        "Core": "#fdcb6e",   "Flexibility": "#55efc4",
    }
    fig = go.Figure(go.Pie(
        labels=list(cats.keys()),
        values=list(cats.values()),
        hole=0.5,
        marker=dict(
            colors=[cat_colors.get(k, "#74b9ff") for k in cats],
            line=dict(color="#0d0d1a", width=2),
        ),
        textfont=dict(color="white"),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="white"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=30, b=10),
        height=280,
        title=dict(text="Time by Category (min)", font=dict(color="white", size=14)),
    )
    return fig


# ── main renderer ─────────────────────────────────────────────
def render_workout_analyzer():
    db = load_exercise_db()
    default_weight = float(st.session_state.user_profile.get("weight", 70))

    st.markdown(
        '<h2 class="grad-text">NLP Workout Analyzer</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#7777aa;">Type your workout in plain English. '
        'The NLP engine extracts exercises, volume and estimates calories burned.</p>',
        unsafe_allow_html=True,
    )

    tab_analyze, tab_log = st.tabs(["Analyze Workout", "Workout Log"])

    # ── TAB 1: Analyze ───────────────────────────────────────
    with tab_analyze:

        # ── Input section ─────────────────────────────────
        st.markdown("### Enter Your Workout")

        EXAMPLES = {
            "-- Choose an example --": "",
            "Strength session":
                "3 sets x 10 pushups, 4 sets x 8 pullups, 3 sets x 12 squats, 3 sets x 10 lunges",
            "Cardio + Core":
                "ran 5km in 30 minutes, 3 sets of 15 crunches, plank for 2 minutes, 50 jumping jacks",
            "Gym workout":
                "bench press 4 sets x 8 reps, bicep curls 3 sets x 12, tricep dips 3 sets x 10, shoulder press 3 sets x 10",
            "Cycling + Strength":
                "cycling 45 minutes, 5 sets x 10 lunges, 100 jumping jacks, 3 sets x 15 crunches",
        }

        ex_choice = st.selectbox(
            "Load an example workout:",
            list(EXAMPLES.keys()),
            key="ex_pick",
        )
        prefill = EXAMPLES[ex_choice]

        workout_text = st.text_area(
            "Your workout log:",
            value=prefill,
            height=130,
            placeholder=(
                "e.g. 3 sets x 10 pushups, ran 5km in 30 minutes, "
                "bench press 4 sets x 8 reps, cycling 45 minutes..."
            ),
            key="workout_txt",
        )

        wt = st.number_input(
            "Your body weight (kg) — for calorie calculation",
            min_value=30.0,
            max_value=200.0,
            value=default_weight,
            step=0.5,
            key="body_wt",
        )

        analyze_btn = st.button("Analyze Workout", type="primary", key="analyze_btn")

        # ── Results ────────────────────────────────────────
        if analyze_btn:
            if not workout_text.strip():
                st.warning("Please enter your workout text above.")
            else:
                exercises = parse_workout_text(workout_text, db)

                if not exercises:
                    st.error(
                        "No exercises could be detected in your text.\n\n"
                        "**Tips:**\n"
                        "- Use exercise names like: pushup, squat, pullup, running, cycling, plank, burpee\n"
                        "- Format: `3 sets x 10 pushups` or `ran 5km in 30 minutes`\n"
                        "- Try loading one of the example workouts above!"
                    )
                else:
                    total_cal = calc_calories_burned(exercises, wt)
                    total_dur = sum(ex["duration"] for ex in exercises)
                    total_vol = sum(ex["sets"] * ex["reps"] for ex in exercises
                                   if ex["category"] != "Cardio")

                    st.success(
                        f"Detected **{len(exercises)} exercises** | "
                        f"Est. duration: **{total_dur:.0f} min** | "
                        f"Calories burned: **{total_cal:.0f} kcal**"
                    )

                    # KPI row
                    k1, k2, k3, k4 = st.columns(4)
                    k1.metric("Exercises",      len(exercises))
                    k2.metric("Total Duration", f"{total_dur:.0f} min")
                    k3.metric("Calories Burned",f"{total_cal:.0f} kcal")
                    k4.metric("Total Volume",   f"{total_vol} reps")

                    st.markdown("---")

                    # Charts side by side
                    ch1, ch2 = st.columns(2)
                    with ch1:
                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        st.plotly_chart(make_workout_bar(exercises, wt), use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                    with ch2:
                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        st.plotly_chart(make_category_pie(exercises), use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                    # Exercise detail cards
                    st.markdown("### Detected Exercises")
                    cat_tag = {
                        "Cardio": "tag-red", "Strength": "tag-purple",
                        "Core": "tag-orange", "Flexibility": "tag-green",
                    }

                    for ex in exercises:
                        kcal = round(ex["met"] * wt * ex["duration"] / 60.0, 1)
                        tag  = cat_tag.get(ex["category"], "tag-blue")
                        dist_str = (
                            f' &nbsp;<span class="tag tag-blue">{ex["distance_km"]} km</span>'
                            if ex["distance_km"] > 0 else ""
                        )
                        st.markdown(
                            f'<div class="glass-card" style="padding:1rem;margin:0.4rem 0;">'
                            f'<b style="font-size:1rem;">{ex["exercise"]}</b>'
                            f'&nbsp;&nbsp;<span class="tag {tag}">{ex["category"]}</span>'
                            f'<span class="tag tag-orange">Duration: {ex["duration"]} min</span>'
                            f'<span class="tag tag-red">Burned: {kcal} kcal</span>'
                            f'{dist_str}<br>'
                            f'<span style="color:#7777aa;font-size:0.85rem;">'
                            f'Sets: {ex["sets"]} &nbsp;|&nbsp; Reps: {ex["reps"]} '
                            f'&nbsp;|&nbsp; Muscles: {ex["muscle"]}</span>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

                    st.markdown("<br>", unsafe_allow_html=True)

                    # Save button
                    if st.button("Save to Workout Log", type="primary", key="save_btn"):
                        st.session_state.workout_log.append({
                            "date":            datetime.now().strftime("%b %d, %H:%M"),
                            "exercises":       exercises,
                            "total_duration":  round(total_dur, 1),
                            "calories_burned": total_cal,
                            "raw_text":        workout_text,
                        })
                        st.success("Workout saved to log!")
                        st.balloons()

    # ── TAB 2: Log ───────────────────────────────────────────
    with tab_log:
        log = st.session_state.workout_log

        if not log:
            st.markdown(
                '<div class="info-box">No workouts logged yet. '
                'Analyze a workout in the first tab and save it here.</div>',
                unsafe_allow_html=True,
            )
        else:
            total_burned = sum(w["calories_burned"] for w in log)
            total_time   = sum(w["total_duration"]  for w in log)

            lc1, lc2, lc3 = st.columns(3)
            lc1.metric("Total Sessions",       len(log))
            lc2.metric("Total Cals Burned",    f"{total_burned:.0f} kcal")
            lc3.metric("Total Training Time",  f"{total_time:.0f} min")

            st.markdown("---")

            for w in reversed(log):
                ex_names = ", ".join(e["exercise"] for e in w["exercises"])
                st.markdown(
                    f'<div class="glass-card" style="padding:1rem;margin:0.4rem 0;">'
                    f'<b>{w["date"]}</b>&nbsp;&nbsp;'
                    f'<span class="tag tag-red">Burned: {w["calories_burned"]} kcal</span>'
                    f'<span class="tag tag-blue">Duration: {w["total_duration"]} min</span>'
                    f'<span class="tag tag-purple">Exercises: {len(w["exercises"])}</span><br>'
                    f'<span style="color:#9999cc;font-size:0.85rem;">{ex_names}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Clear Workout Log", key="clr_workout"):
                st.session_state.workout_log = []
                st.rerun()
