import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-seaworthiness-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///seaworthiness.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Path settings
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    
    # ML settings
    MODELS_DIR = os.path.join(BASE_DIR, 'models')
    SVM_MODEL_PATH = os.path.join(MODELS_DIR, 'svm_model.pkl')
    SCALER_PATH = os.path.join(MODELS_DIR, 'scaler.pkl')
    
    @staticmethod
    def init_app(app):
        # Create necessary directories
        for directory in [Config.DATASET_DIR, Config.UPLOAD_FOLDER, Config.MODELS_DIR]:
            os.makedirs(directory, exist_ok=True)
