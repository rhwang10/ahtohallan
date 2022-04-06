from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from app.db.base_class import Base

class MessageSentiments(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    discord_id = Column(Integer, index=True)
    content = Column(String(1024), nullable=False)
    document_sentiment = Column(DOUBLE_PRECISION, nullable=False)
    document_sentiment_label = Column(String(1024), nullable=False)
    document_emotion_sadness = Column(DOUBLE_PRECISION, nullable=False)
    document_emotion_joy = Column(DOUBLE_PRECISION, nullable=False)
    document_emotion_fear = Column(DOUBLE_PRECISION, nullable=False)
    document_emotion_disgust = Column(DOUBLE_PRECISION, nullable=False)
    document_emotion_anger = Column(DOUBLE_PRECISION, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
