import joblib
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score
import os

class SVMClassifier:
    def __init__(self, model_path, scaler_path=None):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.scaler = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            # Inisialisasi model kosong jika belum ada
            self.model = SVC(kernel='linear', probability=True)
            
        if self.scaler_path and os.path.exists(self.scaler_path):
            self.scaler = joblib.load(self.scaler_path)
        else:
            self.scaler = None

    def train(self, X_train, y_train):
        """
        Melatih model SVM dengan data training
        """
        self.model.fit(X_train, y_train)
        self.save_model()

    def evaluate(self, X_test, y_test):
        """
        Mengevaluasi model dan mengembalikan metrik akurasi, presisi, dan recall
        """
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, pos_label="Baik", zero_division=0)
        rec = recall_score(y_test, y_pred, pos_label="Baik", zero_division=0)
        return acc, prec, rec

    def predict(self, features):
        """
        Memprediksi kelas dari satu set fitur HOG
        Return: "Baik" atau "Rusak"
        """
        if self.model is None or not hasattr(self.model, "classes_"):
            raise ValueError("Model belum dilatih atau tidak ditemukan.")
            
        features_scaled = [features]
        if self.scaler is not None:
            features_scaled = self.scaler.transform(features_scaled)
            
        prediction = self.model.predict(features_scaled)[0]
        
        # Map output to "Baik" or "Rusak"
        # Berdasarkan notebook: Baik = 1, Rusak = 0
        if prediction == 1 or prediction == "1":
            return "Baik"
        elif prediction == 0 or prediction == "0":
            return "Rusak"
        else:
            return prediction

    def save_model(self):
        joblib.dump(self.model, self.model_path)

