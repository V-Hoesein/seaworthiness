import os
from werkzeug.utils import secure_filename
from app.ml.hog_extractor import HOGFeatureExtractor
from app.ml.svm_model import SVMClassifier
from app.config import Config
from app.models.gambar_kapal import GambarKapal
from app.repositories.kapal_repository import GambarKapalRepository

class MLService:
    def __init__(self):
        self.hog_extractor = HOGFeatureExtractor()
        self.svm_classifier = SVMClassifier(Config.SVM_MODEL_PATH, Config.SCALER_PATH)
        self.gambar_repo = GambarKapalRepository()

    def process_and_predict(self, kapal_id, file):
        """
        1. Save uploaded file
        2. Extract features
        3. Predict
        4. Save to database
        """
        if not file:
            raise ValueError("No file provided")

        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)

        try:
            # Extract features
            features = self.hog_extractor.extract_features(filepath)
            
            # Predict
            prediction = self.svm_classifier.predict(features)
            
            # Save to DB
            gambar = GambarKapal(
                kapal_id=kapal_id,
                image_path=filename,
                svm_result=prediction
            )
            self.gambar_repo.save(gambar)
            
            return prediction, filename
            
        except Exception as e:
            # Clean up file if failed
            if os.path.exists(filepath):
                os.remove(filepath)
            raise e
