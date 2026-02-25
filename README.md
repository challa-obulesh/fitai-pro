# 💪 FitAI Pro — Multi-Modal Smart Fitness Meal & Workout Planner

A powerful AI-powered Streamlit web app that combines **Computer Vision**, **NLP**, and **Machine Learning** to provide personalized meal and workout planning.

## 🌐 Live Demo
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

---

## 🚀 Features

| Module | Description | Tech |
|--------|-------------|------|
| 🍽️ **Meal Image Detector** | Upload food photos → AI detects food → instant macros | PIL + Food DB |
| 🏋️ **NLP Workout Analyzer** | Log workouts in plain English → extract exercises → calories burned | Regex NLP + MET |
| 🔥 **Health & Calorie AI** | BMI, BMR, TDEE + personalised macro targets | Mifflin-St Jeor |
| 📊 **Fitness Dashboard** | Interactive calorie balance, weight trend, macro charts | Plotly |
| 📅 **Smart Planner** | Auto-generate weekly meal & workout plans | Rule-based AI |

---

## 📁 Project Structure

```
fitness_planner/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Dependencies
├── src/
│   ├── meal_detector.py    # Module 1: Meal Image Nutrition Detector
│   ├── workout_analyzer.py # Module 2: NLP Workout Analyzer
│   ├── health_predictor.py # Module 3: Health & Calorie Predictor
│   ├── visualization.py    # Module 4: Fitness Dashboard
│   └── user_planner.py     # Module 5: Smart Planner
└── data/
    ├── food_nutrition.json # 30 foods with full macro data
    └── exercises.json      # 20 exercises with MET values
```

---

## 🛠️ Run Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/fitai-pro.git
cd fitai-pro

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 🧠 How It Works

### Meal Detection
- Upload a meal image
- PIL analyses dominant color profile (RGB channels)
- Maps to likely food categories from a 30-food nutrition database
- Calculates calories, protein, carbs, fat for your serving size

### Workout NLP
- Type workouts in natural language: *"3 sets x 10 pushups, ran 5km in 30 minutes"*
- Regex + keyword matching extracts: exercise, sets, reps, duration
- MET (Metabolic Equivalent) formula calculates calories burned:
  `Calories = MET × weight(kg) × time(hours)`

### Health Predictor
- **BMR** using Mifflin-St Jeor equation
- **TDEE** = BMR × Activity Factor
- **Calorie target** adjusted by fitness goal (±250–500 kcal)
- **Macro split** optimised per goal (Weight Loss / Maintain / Muscle Gain)

---

## 📦 Dependencies

- `streamlit` — UI framework
- `plotly` — interactive charts
- `pandas` + `numpy` — data processing
- `pillow` — image processing
- `scikit-learn` — ML utilities

---

## 👨‍💻 Author

Built with ❤️ using Streamlit + Python

---

## 📄 License

MIT License — free to use, modify and share.
