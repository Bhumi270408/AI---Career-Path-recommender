from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

app = Flask(__name__, template_folder='.', static_folder='.', static url_path=' )

FEATURES = [
    "python", "coding", "math", "communication", "creativity",
    "problem_solving", "tech_interest", "business_interest",
    "design_interest", "helping_interest"
]

CAREERS = {
    "AI / ML Engineer": {
        "skills": {"python": 4, "math": 4, "problem_solving": 4, "coding": 4},
        "interests": {"tech_interest": 5},
        "summary": "Build intelligent systems that learn from data and help solve complex problems.",
        "roadmap": ["Learn Python fundamentals and OOP", "Study NumPy, Pandas and data visualization", "Learn statistics and core machine-learning concepts", "Build projects with scikit-learn", "Explore deep learning and model deployment"],
        "roles": ["Junior ML Engineer", "Data Science Intern", "AI Engineer"]
    },
    "Software Developer": {
        "skills": {"coding": 5, "problem_solving": 4, "communication": 3},
        "interests": {"tech_interest": 5},
        "summary": "Design, build and maintain applications, websites and software systems.",
        "roadmap": ["Strengthen one programming language", "Learn data structures and algorithms", "Build web or app projects", "Learn databases, APIs and Git", "Practice testing and collaborative development"],
        "roles": ["Software Developer", "Frontend Developer", "Backend Developer"]
    },
    "Data Analyst": {
        "skills": {"math": 4, "communication": 4, "problem_solving": 4, "python": 3},
        "interests": {"business_interest": 4, "tech_interest": 4},
        "summary": "Turn raw data into clear insights that help people make better decisions.",
        "roadmap": ["Learn Excel or Google Sheets", "Learn SQL", "Practice Python with Pandas and NumPy", "Create dashboards and visualizations", "Build case studies using public datasets"],
        "roles": ["Data Analyst", "Business Intelligence Intern", "Reporting Analyst"]
    },
    "Cloud Engineer": {
        "skills": {"problem_solving": 4, "coding": 3, "communication": 3},
        "interests": {"tech_interest": 5},
        "summary": "Help teams run applications and infrastructure reliably on cloud platforms.",
        "roadmap": ["Learn Linux and command-line basics", "Understand networking fundamentals", "Learn Git and cloud concepts", "Explore AWS, Azure or Google Cloud core services", "Practice Docker, CI/CD and monitoring"],
        "roles": ["Cloud Support Associate", "Cloud Engineer Intern", "DevOps Intern"]
    },
    "Cybersecurity Analyst": {
        "skills": {"problem_solving": 5, "coding": 3, "math": 3},
        "interests": {"tech_interest": 5},
        "summary": "Help protect systems and information by identifying risks and improving security.",
        "roadmap": ["Learn networking and operating-system basics", "Understand security principles and common threats", "Practice Linux fundamentals", "Study defensive monitoring and incident response", "Use legal labs and beginner security projects"],
        "roles": ["SOC Analyst Intern", "Security Analyst", "GRC Intern"]
    },
    "UI / UX Designer": {
        "skills": {"creativity": 5, "communication": 4, "problem_solving": 3},
        "interests": {"design_interest": 5},
        "summary": "Create digital experiences that are useful, accessible and easy to understand.",
        "roadmap": ["Learn design principles and visual hierarchy", "Study user research and accessibility", "Practice wireframes and prototypes", "Build a small portfolio", "Test designs with real users and iterate"],
        "roles": ["UI Designer", "UX Design Intern", "Product Design Intern"]
    },
    "Product Manager": {
        "skills": {"communication": 5, "problem_solving": 4, "creativity": 3},
        "interests": {"business_interest": 5},
        "summary": "Connect user needs, business goals and engineering teams to shape products.",
        "roadmap": ["Understand how digital products are built", "Practice user research and problem framing", "Learn prioritization and product metrics", "Write clear product requirements", "Create a product case study"],
        "roles": ["Associate Product Intern", "Product Analyst", "Program Coordinator"]
    },
    "Business Analyst": {
        "skills": {"communication": 5, "math": 3, "problem_solving": 4},
        "interests": {"business_interest": 5},
        "summary": "Understand business problems, analyze information and recommend practical improvements.",
        "roadmap": ["Build spreadsheet skills", "Learn basic statistics and SQL", "Practice process mapping and requirement gathering", "Create dashboards and concise reports", "Prepare business case studies"],
        "roles": ["Business Analyst Intern", "Operations Analyst", "Business Intelligence Intern"]
    },
    "Full-Stack Developer": {
        "skills": {"coding": 5, "problem_solving": 4, "creativity": 3},
        "interests": {"tech_interest": 5, "design_interest": 3},
        "summary": "Build both the user-facing and server-side parts of web applications.",
        "roadmap": ["Learn HTML, CSS and JavaScript", "Build responsive frontend projects", "Learn a backend framework and REST APIs", "Understand databases and authentication", "Deploy a complete full-stack project"],
        "roles": ["Web Developer Intern", "Frontend Developer", "Full-Stack Developer"]
    },
    "Technical Content Creator": {
        "skills": {"communication": 5, "creativity": 5},
        "interests": {"helping_interest": 4, "tech_interest": 3},
        "summary": "Explain technical ideas through tutorials, documentation and educational content.",
        "roadmap": ["Choose a technical topic to explain", "Practice clear writing and storytelling", "Learn basic documentation tools", "Publish tutorials or project walkthroughs", "Build a small public portfolio"],
        "roles": ["Technical Writer Intern", "Developer Advocate Intern", "Documentation Associate"]
    }
}

def make_training_data(samples_per_career=180, seed=42):
    rng = np.random.default_rng(seed)
    rows, labels = [], []
    for career, profile in CAREERS.items():
        base = {f: 2.5 for f in FEATURES}
        for k, v in profile["skills"].items():
            base[k] = v
        for k, v in profile["interests"].items():
            base[k] = v
        for _ in range(samples_per_career):
            row = {f: float(np.clip(rng.normal(base[f], 1.05), 0, 5)) for f in FEATURES}
            rows.append(row)
            labels.append(career)
    return pd.DataFrame(rows), np.array(labels)

X, y = make_training_data()
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
model = Pipeline([
    ("scale", StandardScaler()),
    ("classifier", RandomForestClassifier(n_estimators=220, random_state=42, class_weight="balanced"))
])
model.fit(X_train, y_train)
MODEL_ACCURACY = accuracy_score(y_test, model.predict(X_test))

# Save a transparent demo dataset so learners can inspect the Pandas-ready data.
dataset = X.copy()
dataset["career_label"] = y
dataset.to_csv("career_training_data.csv", index=False)

@app.route("/")
def home():
    return render_template("index.html", model_accuracy=round(MODEL_ACCURACY * 100, 1))

@app.route("/recommend", methods=["POST"])
def recommend():
    payload = request.get_json(silent=True) or {}
    try:
        values = {feature: float(payload.get(feature, 2.5)) for feature in FEATURES}
    except (TypeError, ValueError):
        return jsonify({"error": "Please enter valid ratings from 0 to 5."}), 400

    if any(v < 0 or v > 5 for v in values.values()):
        return jsonify({"error": "Ratings must be between 0 and 5."}), 400

    user_df = pd.DataFrame([values], columns=FEATURES)
    probabilities = model.predict_proba(user_df)[0]
    classes = model.named_steps["classifier"].classes_
    ranked = sorted(zip(classes, probabilities), key=lambda item: item[1], reverse=True)[:3]

    results = []
    for career, probability in ranked:
        profile = CAREERS[career]
        required = profile["skills"]
        gaps = [
            {"skill": skill.replace("_", " ").title(), "current": round(values[skill], 1), "target": target}
            for skill, target in required.items() if values[skill] < target
        ]
        strengths = [
            skill.replace("_", " ").title()
            for skill in required if values[skill] >= required[skill]
        ]
        results.append({
            "career": career,
            "match": round(float(probability) * 100, 1),
            "summary": profile["summary"],
            "roadmap": profile["roadmap"],
            "roles": profile["roles"],
            "gaps": gaps[:4],
            "strengths": strengths[:4]
        })

    return jsonify({
        "recommendations": results,
        "note": "This is an educational demo trained on a generated sample dataset. Treat matches as exploration suggestions, not a career decision or guarantee."
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok", "model": "RandomForestClassifier", "test_accuracy_demo": round(MODEL_ACCURACY * 100, 1)})

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
