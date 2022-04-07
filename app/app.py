# FastAPI and starlette
from fastapi import FastAPI, APIRouter, Depends
from fastapi.security import HTTPBearer
from starlette.responses import Response
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

import functools
import os
import json

# Requests
from requests.auth import HTTPBasicAuth

# SQLAlchemy
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine

# App imports
from app.schemas.sentiment import MessageSentimentCreate, MessageSentiment
from app.services.watson import WatsonNLUService
from app.sql.message_sentiments import insertMessageSentiment
from app.transformers.emojis import EmojiTransformer
from app.transformers.urls import UrlTransformer

app = FastAPI()
watson = WatsonNLUService()
emojis = EmojiTransformer()
urls = UrlTransformer()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.post("/sentiment")
async def createSentiment(sentimentCreate: MessageSentimentCreate,
                          persist: bool = False,
                          db: Session = Depends(get_db),
                          response_model=MessageSentiment):

    urlsReplaced = urls.transform(sentimentCreate.content).strip()

    if not urlsReplaced:
        return Response(json.dumps({"status": "no input"}), status_code=HTTP_200_OK)

    sentimentReplaced = emojis.transform(urlsReplaced)

    watsonResp = await watson.getSentiment(sentimentReplaced)

    messageSentiment = MessageSentiment(
        discord_id=sentimentCreate.discord_id,
        content=sentimentCreate.content,
        document_sentiment=watsonResp["sentiment"]["document"]["score"],
        document_sentiment_label=watsonResp["sentiment"]["document"]["label"],
        document_emotion_sadness=watsonResp["emotion"]["document"]["emotion"]["sadness"],
        document_emotion_joy=watsonResp["emotion"]["document"]["emotion"]["joy"],
        document_emotion_fear=watsonResp["emotion"]["document"]["emotion"]["fear"],
        document_emotion_disgust=watsonResp["emotion"]["document"]["emotion"]["disgust"],
        document_emotion_anger=watsonResp["emotion"]["document"]["emotion"]["anger"]
    )

    if persist:
        insertMessageSentiment(db, messageSentiment)

    return messageSentiment
