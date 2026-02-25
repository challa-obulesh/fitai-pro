"""
Module 1 - Meal Image Nutrition Detector
Analyzes uploaded food images using PIL color profiling + food database lookup.
"""
import json
import streamlit as st
import numpy as np
from PIL import Image
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go

# ── data ──────────────────────────────────────────────────────
_DB_PATH = Path(__file__).parent.parent / "data" / "food_nutrition.json"


@st.cache_data
def load_food_db():
    with open(_DB_PATH, encoding="utf-8") as f:
        return json.load(f)


# ── image analysis helper ─────────────────────────────────────
def analyse_image_colors(img):
    """Return dominant color profile and food suggestion hints from image."""
    img_small = img.convert("RGB").resize((64, 64))
    arr = np.array(img_small, dtype=float)
    r = arr[:, :, 0].mean()
    g = arr[:, :, 1].mean()
    b = arr[:, :, 2].mean()
    brightness = (r + g + b) / 3
    warm  = r / (b + 1)
    green = g / ((r + b) / 2 + 1)

    if green > 1.3:
        hints = ["Spinach", "Broccoli", "Mixed Salad"]
    elif warm > 1.4 and brightness > 140:
        hints = ["Grilled Chicken Breast", "French Fries", "Sweet Potato"]
    elif warm > 1.2 and brightness < 140:
        hints = ["Burger", "Grilled Chicken Breast", "Salmon Fillet"]
    elif brightness > 180:
        hints = ["White Rice (cooked)", "Greek Yogurt", "Oatmeal (cooked)"]
    elif brightness < 90:
        hints = ["Dal (Lentils)", "Brown Rice (cooked)", "Pasta (cooked)"]
    else:
        hints = ["Grilled Chicken Breast", "White Rice (cooked)", "Broccoli"]

    return {"r": r, "g": g, "b": b, "brightness": brightness, "hints": hints}


# ── macro donut chart ─────────────────────────────────────────
def make_macro_chart(protein, carbs, fat):
    # guard against all-zero values
    if protein + carbs + fat == 0:
        protein, carbs, fat = 1, 1, 1

    fig = go.Figure(go.Pie(
        labels=["Protein", "Carbs", "Fat"],
        values=[protein, carbs, fat],
        hole=0.55,
        marker=dict(
            colors=["#a29bfe", "#fd79a8", "#fdcb6e"],
            line=dict(color="#0d0d1a", width=2),
        ),
        textfont=dict(color="white"),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(font=dict(color="white"), bgcolor="rgba(0,0,0,0)"),
        height=280,
    )
    return fig


# ── helper: render nutrition badges ──────────────────────────
def _nutrition_badges(cal, prot, carbs, fat):
    badge_cols = st.columns(4)
    items = [
        (badge_cols[0], f"{cal:.0f}",     "kcal",    "#fd79a8"),
        (badge_cols[1], f"{prot:.1f}g",   "protein", "#a29bfe"),
        (badge_cols[2], f"{carbs:.1f}g",  "carbs",   "#fdcb6e"),
        (badge_cols[3], f"{fat:.1f}g",    "fat",     "#55efc4"),
    ]
    for bcol, val, lbl, clr in items:
        with bcol:
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.04);'
                f'border:1px solid {clr}44;border-radius:12px;'
                f'padding:0.8rem;text-align:center;">'
                f'<div style="font-size:1.3rem;font-weight:800;color:{clr}">{val}</div>'
                f'<div style="font-size:0.75rem;color:#7777aa">{lbl}</div></div>',
                unsafe_allow_html=True,
            )


# ── main renderer ─────────────────────────────────────────────
def render_meal_detector():
    db = load_food_db()

    st.markdown(
        '<h2 class="grad-text">Meal Image Nutrition Detector</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#7777aa;">Upload a meal photo — the AI analyses colours &amp; texture, '
        'suggests likely foods, then computes full nutrition from our database.</p>',
        unsafe_allow_html=True,
    )

    tab_upload, tab_manual, tab_log = st.tabs(
        ["Image Analysis", "Manual Entry", "Today's Food Log"]
    )

    # ── TAB 1: Image Upload & Analysis ───────────────────────
    with tab_upload:
        st.markdown("### Upload Your Meal Photo")

        uploaded = st.file_uploader(
            "Choose a meal image",
            type=["jpg", "jpeg", "png", "webp"],
            key="meal_uploader",
        )

        serving = st.number_input(
            "Serving size (grams)",
            min_value=10, max_value=2000,
            value=150, step=10,
            key="serving_img",
        )

        if uploaded is not None:
            # open image once and reuse
            img = Image.open(uploaded)

            col_img, col_res = st.columns([1, 1])

            with col_img:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("**Uploaded Image**")
                st.image(img, caption="Your meal", width=450)
                st.markdown("</div>", unsafe_allow_html=True)

            with col_res:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("**AI Food Detection**")

                color_info = analyse_image_colors(img)
                r_val = int(color_info["r"])
                g_val = int(color_info["g"])
                b_val = int(color_info["b"])

                st.markdown(
                    f'<div style="background:rgb({r_val},{g_val},{b_val});'
                    f'height:16px;border-radius:6px;margin-bottom:0.5rem;"></div>'
                    f'<p style="color:#7777aa;font-size:0.8rem;">Dominant colour: '
                    f'RGB({r_val},{g_val},{b_val}) | Brightness: {color_info["brightness"]:.0f}</p>',
                    unsafe_allow_html=True,
                )

                st.markdown("**Suggested Foods (based on image):**")

                # build option list: AI hints first, then full db
                all_options = color_info["hints"] + [
                    k for k in sorted(db.keys()) if k not in color_info["hints"]
                ]

                hint_food = st.selectbox(
                    "Select or confirm food:",
                    options=all_options,
                    key="hint_sel",
                )

                if hint_food and hint_food in db:
                    food_data = db[hint_food]
                    factor = serving / 100.0

                    cal   = food_data["calories"] * factor
                    prot  = food_data["protein"]  * factor
                    carbs = food_data["carbs"]    * factor
                    fat   = food_data["fat"]      * factor
                    fib   = food_data["fiber"]    * factor

                    st.markdown("---")
                    _nutrition_badges(cal, prot, carbs, fat)
                    st.plotly_chart(
                        make_macro_chart(prot, carbs, fat),
                        use_container_width=True,
                    )

                    category    = food_data.get("category", "Food")
                    food_emoji  = food_data.get("emoji", "")
                    cat_tag_map = {
                        "Protein": "tag-purple", "Dairy": "tag-blue",
                        "Carbs": "tag-orange",   "Vegetables": "tag-green",
                        "Fruits": "tag-green",   "Fats": "tag-red",
                        "Fast Food": "tag-red",  "Legumes": "tag-green",
                        "Supplements": "tag-blue",
                    }
                    cat_tag = cat_tag_map.get(category, "tag-blue")
                    st.markdown(
                        f'<span class="tag {cat_tag}">{category}</span>'
                        f'<span class="tag tag-purple">{food_emoji} {hint_food}</span>'
                        f'<span class="tag tag-green">Fiber {fib:.1f}g</span>',
                        unsafe_allow_html=True,
                    )

                    if st.button("Add to Food Log", type="primary", key="add_img"):
                        st.session_state.food_log.append({
                            "food":     hint_food,
                            "serving":  serving,
                            "calories": round(cal, 1),
                            "protein":  round(prot, 1),
                            "carbs":    round(carbs, 1),
                            "fat":      round(fat, 1),
                            "fiber":    round(fib, 1),
                            "time":     datetime.now().strftime("%H:%M"),
                        })
                        st.success(f"{hint_food} added to your food log!")

                st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.markdown(
                '<div class="info-box">Upload a meal image above to get started with AI nutrition detection.</div>',
                unsafe_allow_html=True,
            )

    # ── TAB 2: Manual Entry ───────────────────────────────────
    with tab_manual:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Log Food Manually")

        mc1, mc2 = st.columns(2)
        with mc1:
            food_sel = st.selectbox(
                "Select food item",
                sorted(db.keys()),
                key="man_food",
            )
        with mc2:
            serving_man = st.number_input(
                "Serving (grams)",
                min_value=10, max_value=2000,
                value=150, step=10,
                key="serving_man",
            )

        if food_sel and food_sel in db:
            food_data = db[food_sel]
            fac = serving_man / 100.0

            st.markdown("---")
            n1, n2, n3, n4, n5 = st.columns(5)
            n1.metric("Calories",  f"{food_data['calories'] * fac:.0f} kcal")
            n2.metric("Protein",   f"{food_data['protein']  * fac:.1f} g")
            n3.metric("Carbs",     f"{food_data['carbs']    * fac:.1f} g")
            n4.metric("Fat",       f"{food_data['fat']      * fac:.1f} g")
            n5.metric("Fiber",     f"{food_data['fiber']    * fac:.1f} g")

            # macro chart
            st.plotly_chart(
                make_macro_chart(
                    food_data["protein"] * fac,
                    food_data["carbs"]   * fac,
                    food_data["fat"]     * fac,
                ),
                use_container_width=True,
            )

            if st.button("Add to Log", type="primary", key="add_man"):
                st.session_state.food_log.append({
                    "food":     food_sel,
                    "serving":  serving_man,
                    "calories": round(food_data["calories"] * fac, 1),
                    "protein":  round(food_data["protein"]  * fac, 1),
                    "carbs":    round(food_data["carbs"]    * fac, 1),
                    "fat":      round(food_data["fat"]       * fac, 1),
                    "fiber":    round(food_data["fiber"]    * fac, 1),
                    "time":     datetime.now().strftime("%H:%M"),
                })
                st.success(f"{food_sel} ({serving_man}g) added to log!")

        st.markdown("</div>", unsafe_allow_html=True)

    # ── TAB 3: Food Log ───────────────────────────────────────
    with tab_log:
        log = st.session_state.food_log

        if not log:
            st.markdown(
                '<div class="info-box">No meals logged yet. '
                'Use Image Analysis or Manual Entry to add meals.</div>',
                unsafe_allow_html=True,
            )
        else:
            import pandas as pd
            df = pd.DataFrame(log)

            lc1, lc2, lc3, lc4 = st.columns(4)
            lc1.metric("Total Calories", f"{df['calories'].sum():.0f} kcal")
            lc2.metric("Total Protein",  f"{df['protein'].sum():.1f} g")
            lc3.metric("Total Carbs",    f"{df['carbs'].sum():.1f} g")
            lc4.metric("Total Fat",      f"{df['fat'].sum():.1f} g")

            st.markdown("---")

            for row in log:
                st.markdown(
                    f'<div class="glass-card" style="padding:1rem;">'
                    f'<b>{row["time"]} &mdash; {row["food"]}</b>'
                    f'&nbsp;<span class="tag tag-orange">Weight: {row["serving"]}g</span>'
                    f'<span class="tag tag-red">Calories: {row["calories"]} kcal</span>'
                    f'<span class="tag tag-purple">Protein: {row["protein"]}g</span>'
                    f'<span class="tag tag-blue">Carbs: {row["carbs"]}g</span>'
                    f'<span class="tag tag-green">Fat: {row["fat"]}g</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Clear Food Log", key="clear_food"):
                st.session_state.food_log = []
                st.rerun()
