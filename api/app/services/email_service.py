from datetime import datetime
from app.models.email import db, EmailRecord

def create_email(sender, recipient, subject, body, is_spam, spam_score, received=None):
    if received is None:
        received = datetime.now()
        
    email = EmailRecord(
        sender=sender,
        recipient=recipient,
        subject=subject,
        body=body,
        received=received,
        is_spam=is_spam,
        spam_score=spam_score
    )
    db.session.add(email)
    db.session.commit()
    return email

def get_all_emails():
    return EmailRecord.query.order_by(EmailRecord.received.desc()).all()
