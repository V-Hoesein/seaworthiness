import joblib
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score
import os

class SVMClassifier:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            # Inisialisasi model kosong jika belum ada
            self.model = SVC(kernel='linear', probability=True)

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
        prediction = self.model.predict([features])
        return prediction[0]

    def save_model(self):
        joblib.dump(self.model, self.model_path)
