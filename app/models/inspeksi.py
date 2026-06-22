from datetime import datetime
from app.extensions import db

class Inspeksi(db.Model):
    __tablename__ = 'inspeksi'

    id = db.Column(db.Integer, primary_key=True)
    kapal_id = db.Column(db.Integer, db.ForeignKey('kapal.id'), nullable=False)
    
    # Nilai boolean / integer untuk komponen administrasi
    apar = db.Column(db.Integer, nullable=False, default=0)
    radio = db.Column(db.Integer, nullable=False, default=0)
    jaket = db.Column(db.Integer, nullable=False, default=0)
    izin = db.Column(db.Integer, nullable=False, default=0)
    mesin = db.Column(db.Integer, nullable=False, default=0)
    
    skor = db.Column(db.Integer, nullable=False, default=0)
    status_kelayakan = db.Column(db.String(20), nullable=False) # "Layak" atau "Tidak Layak"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Inspeksi {self.id} - Status: {self.status_kelayakan}>"
