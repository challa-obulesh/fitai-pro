"""
Module 5 – User Planning UI
Generates personalised weekly meal plans and workout schedules
based on the user's calorie targets and fitness goals.
"""
import streamlit as st
import random


# ── meal templates ────────────────────────────────────────────
MEALS = {
    "Lose": {
        "Breakfast": [
            ("🥣 Oatmeal + Berries",          "Oatmeal (cooked) 80g + Blueberries 60g",  320),
            ("🥚 Boiled Eggs + Spinach",       "Boiled Eggs 2 + Spinach 50g + toast",      280),
            ("🥛 Greek Yogurt Parfait",         "Greek Yogurt 200g + Apple 100g",           250),
        ],
        "Lunch": [
            ("🍗 Grilled Chicken Salad",       "Chicken 150g + Mixed Salad 100g",          320),
            ("🐟 Tuna Wrap",                   "Tuna 100g + Whole Wheat Bread 60g",        360),
            ("🍲 Dal & Brown Rice",             "Dal 150g + Brown Rice 100g",               360),
        ],
        "Dinner": [
            ("🐟 Baked Salmon + Broccoli",     "Salmon 150g + Broccoli 150g",              390),
            ("🍗 Chicken + Sweet Potato",      "Chicken 130g + Sweet Potato 150g",         360),
            ("🥗 Paneer Tikka + Salad",        "Paneer 100g + Mixed Salad 150g",           350),
        ],
        "Snack": [
            ("🥜 Almonds",                     "Almonds 30g",                              173),
            ("🍌 Banana + Greek Yogurt",       "Banana 1 + Greek Yogurt 100g",            148),
            ("💪 Protein Shake",               "Protein Shake 1 scoop (300ml water)",     120),
        ],
    },
    "Gain": {
        "Breakfast": [
            ("🥣 Big Oatmeal Bowl",             "Oatmeal 120g + Banana + Almonds 20g",    520),
            ("🥚 Eggs + Brown Rice",            "Eggs 3 + Brown Rice 100g",               480),
            ("💪 Protein Pancakes",             "Oatmeal 100g + Eggs 2 + Banana",         450),
        ],
        "Lunch": [
            ("🍗 Chicken Rice Bowl",           "Chicken 200g + White Rice 180g",          580),
            ("🐟 Salmon + Quinoa",             "Salmon 180g + Quinoa 150g",              560),
            ("🍝 Pasta + Chicken",             "Pasta 200g + Chicken 150g",              590),
        ],
        "Dinner": [
            ("🏋️ Beef/Paneer + Potato",        "Paneer 150g + Sweet Potato 200g",        620),
            ("🐟 Tuna + Pasta Bowl",           "Tuna 120g + Pasta 180g",                 580),
            ("🍗 Chicken + Avocado Rice",      "Chicken 180g + Rice 150g + Avocado 50g", 610),
        ],
        "Snack": [
            ("🥜 Almonds + Banana",            "Almonds 40g + Banana",                   314),
            ("💪 Mass Shake",                  "Protein Shake + Banana + Milk 200ml",    380),
            ("🧀 Cottage Cheese",              "Cottage Cheese 200g",                    196),
        ],
    },
    "Maintain": {
        "Breakfast": [
            ("🥚 Egg + Toast",                 "Boiled Eggs 2 + Whole Wheat Bread 60g",  370),
            ("🥣 Oatmeal",                     "Oatmeal 100g + Blueberries 80g",         330),
            ("🥛 Yogurt Bowl",                 "Greek Yogurt 180g + Apple + Almonds 15g",325),
        ],
        "Lunch": [
            ("🍗 Chicken + Rice",              "Chicken 130g + Brown Rice 130g",          450),
            ("🍲 Dal + Roti",                  "Dal 150g + Whole Wheat Bread 80g",        430),
            ("🥗 Tuna Salad",                  "Tuna 100g + Mixed Salad 150g",            300),
        ],
        "Dinner": [
            ("🐟 Salmon + Veggies",            "Salmon 140g + Broccoli 150g + Rice 100g",490),
            ("🍗 Grilled Chicken + Quinoa",   "Chicken 140g + Quinoa 120g",              440),
            ("🥗 Paneer Bowl",                 "Paneer 120g + Sweet Potato 150g",         480),
        ],
        "Snack": [
            ("🍎 Apple + Almonds",             "Apple 1 + Almonds 20g",                  168),
            ("🥛 Milk",                        "Milk 300ml",                              183),
            ("💪 Protein Shake",               "Protein Shake 1 scoop",                  120),
        ],
    },
}

WORKOUTS = {
    "Lose": {
        "Monday":    ("💨 HIIT Cardio",   ["Jumping Jacks 3×30", "Burpees 3×15", "Mountain Climbers 3×20", "Jump Rope 5 min"]),
        "Tuesday":   ("💪 Upper Body",     ["Push-ups 4×12", "Pull-ups 3×8", "Shoulder Press 3×12", "Tricep Dips 3×15"]),
        "Wednesday": ("🚴 Steady Cardio",  ["Cycling 45 min @ moderate pace", "Plank 3×60s", "Crunches 3×20"]),
        "Thursday":  ("🦵 Lower Body",     ["Squats 4×15", "Lunges 3×12 each leg", "Deadlift 3×10"]),
        "Friday":    ("🔥 Full Body HIIT", ["Burpees 4×10", "Push-ups 3×15", "Squats 3×20", "Mountain Climbers 3×20"]),
        "Saturday":  ("🏃 Long Run",       ["Running 5-6 km", "Cool-down walk 10 min", "Stretching 10 min"]),
        "Sunday":    ("🧘 Active Rest",    ["Yoga 30 min", "Light walking 20 min", "Foam rolling"]),
    },
    "Gain": {
        "Monday":    ("🏋️ Chest & Triceps", ["Bench Press 4×8", "Incline Push-ups 3×12", "Tricep Dips 4×10", "Cable Flyes 3×12"]),
        "Tuesday":   ("🦵 Legs",             ["Squats 5×8", "Deadlift 4×6", "Leg Press 3×12", "Lunges 3×10 each"]),
        "Wednesday": ("🏋️ Back & Biceps",   ["Pull-ups 4×8", "Rows 4×10", "Bicep Curls 3×12", "Hammer Curls 3×12"]),
        "Thursday":  ("💤 Rest / Light",     ["Walking 30 min", "Stretching 20 min"]),
        "Friday":    ("💪 Shoulders & Core", ["Shoulder Press 4×10", "Lateral Raises 3×15", "Plank 3×60s", "Crunches 3×20"]),
        "Saturday":  ("🔥 Full Body Power",  ["Deadlift 5×5", "Bench Press 4×6", "Squats 4×8", "Pull-ups 3×8"]),
        "Sunday":    ("🧘 Rest",             ["Active recovery", "Light yoga or walk"]),
    },
    "Maintain": {
        "Monday":    ("💨 Cardio",            ["Running 30 min", "Jump Rope 5 min", "Cool-down"]),
        "Tuesday":   ("💪 Strength",          ["Push-ups 3×12", "Squats 3×15", "Plank 3×45s", "Lunges 3×12"]),
        "Wednesday": ("🧘 Flexibility",       ["Yoga 30 min", "Stretching 15 min"]),
        "Thursday":  ("🚴 Cardio Mix",        ["Cycling 30 min", "Burpees 3×10", "Mountain Climbers 2×20"]),
        "Friday":    ("🏋️ Full Body",         ["Deadlift 3×8", "Pull-ups 3×8", "Shoulder Press 3×10"]),
        "Saturday":  ("🏃 Long Walk / Hike",  ["Brisk walk 60 min or nature hike"]),
        "Sunday":    ("💤 Rest",              ["Complete rest or light stretching"]),
    },
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def get_goal_key(goal_str: str) -> str:
    if "Lose" in goal_str: return "Lose"
    if "Bulk" in goal_str or "Gain" in goal_str: return "Gain"
    return "Maintain"


# ── renderer ──────────────────────────────────────────────────
def render_user_planner():
    st.markdown('<h2 class="grad-text">📅 Smart Weekly Planner</h2>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#7777aa;">Auto-generated personalised weekly meal & workout plans aligned with your calorie targets.</p>',
        unsafe_allow_html=True,
    )

    profile = st.session_state.user_profile
    if not profile:
        st.markdown(
            '<div class="warning-box">⚠️ No profile found! '
            'Please set up your profile in <b>Health & Calorie AI</b> first to get personalised plans.</div>',
            unsafe_allow_html=True,
        )
        # still allow with defaults
        tdee     = 2000
        goal_key = "Maintain"
        name     = "User"
    else:
        tdee     = profile.get("tdee", 2000)
        goal_key = get_goal_key(profile.get("goal", "Maintain Weight"))
        name     = profile.get("name", "User")

    tab_meal, tab_workout, tab_goals = st.tabs(
        ["🍽️ Meal Plan", "🏋️ Workout Plan", "🎯 Goals Tracker"]
    )

    # ── MEAL PLAN ───────────────────────────────────────────
    with tab_meal:
        st.markdown(f"#### 🍽️ Weekly Meal Plan for **{name}** · Target: {tdee:.0f} kcal/day")

        per_meal = {"Breakfast": 0.25, "Lunch": 0.35, "Dinner": 0.30, "Snack": 0.10}

        regen = st.button("🔄 Regenerate Plan", key="regen_meal")
        seed_key = "meal_plan_seed"
        if regen or seed_key not in st.session_state:
            st.session_state[seed_key] = random.randint(0, 99999)

        random.seed(st.session_state[seed_key])
        meal_templates = MEALS[goal_key]

        for day in DAYS:
            with st.expander(f"📅 {day}", expanded=(day == DAYS[0])):
                day_meals = {m: random.choice(opts) for m, opts in meal_templates.items()}
                day_total = sum(v[2] for v in day_meals.values())

                cols = st.columns(4)
                for col, (meal_type, (label, desc, kcal)) in zip(cols, day_meals.items()):
                    target_cal = tdee * per_meal[meal_type]
                    tag_color  = "tag-green" if abs(kcal - target_cal) < 80 else "tag-orange"
                    with col:
                        st.markdown(
                            f'<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);'
                            f'border-radius:14px;padding:1rem;min-height:150px;">'
                            f'<div style="color:#7777aa;font-size:0.75rem;font-weight:700;text-transform:uppercase;'
                            f'letter-spacing:0.05em;">{meal_type}</div>'
                            f'<div style="font-size:0.95rem;font-weight:600;color:#e8e8ff;margin:0.4rem 0">{label}</div>'
                            f'<div style="color:#7777aa;font-size:0.78rem;margin-bottom:0.5rem">{desc}</div>'
                            f'<span class="tag {tag_color}">🔥 {kcal} kcal</span>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

                st.markdown(
                    f'<div style="margin-top:0.5rem;font-size:0.85rem;color:#9999cc;">'
                    f'Day total: <b style="color:#a29bfe">{day_total} kcal</b> '
                    f'<span style="color:#7777aa">/ target {tdee:.0f} kcal</span></div>',
                    unsafe_allow_html=True,
                )

    # ── WORKOUT PLAN ────────────────────────────────────────
    with tab_workout:
        st.markdown(f"#### 🏋️ Weekly Workout Plan — Goal: **{goal_key}**")
        workout_templates = WORKOUTS[goal_key]

        wcols = st.columns(7)
        for col, day in zip(wcols, DAYS):
            w_name, exercises = workout_templates[day]
            rest = "Rest" in w_name or "recovery" in w_name.lower()
            card_bg = "rgba(255,255,255,0.02)" if rest else "rgba(162,155,254,0.06)"
            card_border = "rgba(255,255,255,0.06)" if rest else "rgba(162,155,254,0.3)"
            with col:
                st.markdown(
                    f'<div style="background:{card_bg};border:1px solid {card_border};'
                    f'border-radius:14px;padding:0.9rem;min-height:320px;">'
                    f'<div style="font-size:0.75rem;font-weight:700;color:#7777aa;'
                    f'text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.4rem">{day[:3]}</div>'
                    f'<div style="font-size:0.9rem;font-weight:700;color:#a29bfe;margin-bottom:0.7rem">{w_name}</div>'
                    + "".join(
                        f'<div style="font-size:0.77rem;color:#9999cc;padding:0.25rem 0;'
                        f'border-bottom:1px solid rgba(255,255,255,0.05);">• {ex}</div>'
                        for ex in exercises
                    ) +
                    f'</div>',
                    unsafe_allow_html=True,
                )

    # ── GOALS TRACKER ───────────────────────────────────────
    with tab_goals:
        st.markdown("#### 🎯 Your Fitness Goals")

        if not profile:
            st.info("Set up your profile first to track progress against your goals.")
            return

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("**📌 Current Profile**")
            for label, val in [
                ("Name",           profile.get("name", "—")),
                ("Goal",           profile.get("goal", "—")),
                ("Daily Calories", f"{profile.get('tdee',0):.0f} kcal"),
                ("BMI",            f"{profile.get('bmi',0):.1f}"),
                ("Activity",       profile.get("activity","—").split("(")[0].strip()),
            ]:
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;padding:0.5rem 0;'
                    f'border-bottom:1px solid rgba(255,255,255,0.06);">'
                    f'<span style="color:#7777aa">{label}</span>'
                    f'<span style="color:#a29bfe;font-weight:600">{val}</span></div>',
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("**📊 Logging Progress**")
            food_days = len(st.session_state.food_log)
            workout_days = len(st.session_state.workout_log)
            total_cal_in  = sum(i.get("calories",0) for i in st.session_state.food_log)
            total_cal_out = sum(w.get("calories_burned",0) for w in st.session_state.workout_log)

            for label, val in [
                ("Meals Logged",       food_days),
                ("Workouts Logged",    workout_days),
                ("Total Calories In",  f"{total_cal_in:.0f} kcal"),
                ("Total Calories Out", f"{total_cal_out:.0f} kcal"),
                ("Net Balance",        f"{total_cal_in - total_cal_out:+.0f} kcal"),
            ]:
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;padding:0.5rem 0;'
                    f'border-bottom:1px solid rgba(255,255,255,0.06);">'
                    f'<span style="color:#7777aa">{label}</span>'
                    f'<span style="color:#fdcb6e;font-weight:600">{val}</span></div>',
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

        # set a target weight
        st.markdown("---")
        st.markdown("**🎯 Set a Weight Goal**")
        cw = profile.get("weight", 70)
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Current Weight", f"{cw} kg")
        with col_b:
            target_w = st.number_input("Target Weight (kg)", 30.0, 200.0, float(cw), 0.5, key="tgt_w")
        with col_c:
            diff = target_w - cw
            weeks = abs(diff) / 0.3  # ~0.3 kg/week realistic
            st.metric("Est. Timeline", f"{weeks:.0f} weeks", delta=f"{diff:+.1f} kg")

        st.markdown(
            '<div class="success-box">✅ <b>Pro Tip:</b> Aim for 0.25–0.5 kg change per week '
            'for sustainable, healthy progress.</div>',
            unsafe_allow_html=True,
        )
