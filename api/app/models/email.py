from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class EmailRecord(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(256), nullable=False)
    recipient = db.Column(db.String(256), nullable=False)
    subject = db.Column(db.String(512), nullable=False)
    body = db.Column(db.Text, nullable=True)
    received = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_spam = db.Column(db.Boolean, nullable=False, default=False)
    spam_score = db.Column(db.Float, nullable=False, default=0.0)

    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender,
            'recipient': self.recipient,
            'subject': self.subject,
            'body': self.body,
            'received': self.received.isoformat() if self.received else None,
            'is_spam': bool(self.is_spam),
            'spam_score': float(self.spam_score)
        }
