from sqlalchemy.orm import Session

from app.models.message_sentiments import MessageSentiments
from app.schemas.sentiment import MessageSentiment

def insertMessageSentiment(db: Session, messageSentiment: MessageSentiment):
    msgSentiment = MessageSentiments(
        discord_id=messageSentiment.discord_id,
        content=messageSentiment.content,
        document_sentiment=messageSentiment.document_sentiment,
        document_sentiment_label=messageSentiment.document_sentiment_label,
        document_emotion_sadness=messageSentiment.document_emotion_sadness,
        document_emotion_joy=messageSentiment.document_emotion_joy,
        document_emotion_fear=messageSentiment.document_emotion_fear,
        document_emotion_disgust=messageSentiment.document_emotion_disgust,
        document_emotion_anger=messageSentiment.document_emotion_anger
    )
    db.add(msgSentiment)
    db.commit()
