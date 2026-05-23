import os
import joblib
from django.conf import settings

# Path to models folder
MODEL_DIR = os.path.join(settings.BASE_DIR, "ai_engine", "models")

# Global variables
tfidf_vectorizer = None
resume_score_model = None
readiness_model = None


def load_models():
    global tfidf_vectorizer, resume_score_model, readiness_model

    try:
        # Load TF-IDF
        tfidf_path = os.path.join(MODEL_DIR, "tfidf.pkl")
        tfidf_vectorizer = joblib.load(tfidf_path)

        # Load Resume Score Model
        score_model_path = os.path.join(MODEL_DIR, "resume_score_model.pkl")
        resume_score_model = joblib.load(score_model_path)

        # Load Readiness Model
        readiness_model_path = os.path.join(MODEL_DIR, "readiness_model.pkl")
        readiness_model = joblib.load(readiness_model_path)

        print("AI Models Loaded Successfully")

    except Exception as e:
        print("Error loading AI models:", e)


# Load models when file is imported
load_models()
