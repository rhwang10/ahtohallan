from typing import List, Optional

from datetime import datetime

from pydantic import BaseModel

class MessageSentimentBase(BaseModel):
    discord_id: int

class MessageSentimentCreate(MessageSentimentBase):
    content: str

class MessageSentiment(MessageSentimentBase):
    content: str
    document_sentiment: float
    document_sentiment_label: str
    document_emotion_sadness: float
    document_emotion_joy: float
    document_emotion_fear: float
    document_emotion_disgust: float
    document_emotion_anger: float

class MessageSentimentGet(MessageSentiment):
    created_at: datetime
