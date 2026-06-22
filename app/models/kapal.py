from datetime import datetime
from app.extensions import db

class Kapal(db.Model):
    __tablename__ = 'kapal'

    id = db.Column(db.Integer, primary_key=True)
    nama_kapal = db.Column(db.String(100), nullable=False)
    pemilik = db.Column(db.String(100), nullable=False)
    nomor_registrasi = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    gambar = db.relationship('GambarKapal', backref='kapal', lazy=True, cascade="all, delete-orphan")
    inspeksi = db.relationship('Inspeksi', backref='kapal', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Kapal {self.nama_kapal}>"
