# PathPilot — AI Career Path Recommender

A beginner-friendly full-stack demo that recommends career directions from a user's self-rated skills and interests.

## Run locally (Windows)

1. Install Python 3.10 or newer.
2. Extract this ZIP and open the extracted `ai_career_path_recommender` folder in VS Code.
3. Open Terminal in that folder.
4. Create and activate a virtual environment (optional but recommended):

   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```

5. Install dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```

6. Start the website:

   ```powershell
   py app.py
   ```

7. Open the local address printed in the terminal, usually `http://127.0.0.1:5000`.

## Where the three libraries are used

- **NumPy:** generates a sample training dataset with varied skill and interest ratings.
- **Pandas:** stores the training features in a DataFrame and exports `career_training_data.csv`.
- **Scikit-learn:** trains a `RandomForestClassifier`, evaluates it on a held-out test split, and predicts the top three career matches.

## Project structure

```text
ai_career_path_recommender/
├── app.py
├── requirements.txt
├── career_training_data.csv
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Important note

This is an educational prototype. The training labels are generated from illustrative career profiles, not collected from real hiring or career-outcome data. The match percentages are model scores, not scientifically validated probabilities or guarantees. Use the recommendations as ideas to explore, not as a final career decision.

## Quick API check

With the server running, open `http://127.0.0.1:5000/health` to see the model status and demo test score.
