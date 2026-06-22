from datetime import datetime
from app.extensions import db

class GambarKapal(db.Model):
    __tablename__ = 'gambar_kapal'

    id = db.Column(db.Integer, primary_key=True)
    kapal_id = db.Column(db.Integer, db.ForeignKey('kapal.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    svm_result = db.Column(db.String(20), nullable=True) # "Baik" atau "Rusak"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<GambarKapal {self.id} - KapalID: {self.kapal_id}>"
