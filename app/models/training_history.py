from datetime import datetime
from app.extensions import db

class TrainingHistory(db.Model):
    __tablename__ = 'training_history'

    id = db.Column(db.Integer, primary_key=True)
    accuracy = db.Column(db.Float, nullable=False)
    precision = db.Column(db.Float, nullable=False)
    recall = db.Column(db.Float, nullable=False)
    model_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<TrainingHistory {self.id} - Acc: {self.accuracy}>"
