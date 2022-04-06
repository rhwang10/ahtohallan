# FastAPI and starlette
from fastapi import FastAPI, APIRouter, Depends
from fastapi.security import HTTPBearer
from starlette.responses import Response
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

import functools
import os
from requests.auth import HTTPBasicAuth

# SQLAlchemy
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine

# App imports
from app.schemas.sentiment import MessageSentimentCreate, MessageSentiment
from app.services.watson import WatsonNLUService
from app.sql.message_sentiments import insertMessageSentiment

app = FastAPI()
watson = WatsonNLUService()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def _asyncCallable(func, endpoint, data, headers, params=None):

    auth = HTTPBasicAuth("apikey", os.environ.get("IBM_NLU_API_KEY"))

    return functools.partial(
        func, endpoint, data=data, params=params, headers=headers, auth=auth
    )

@app.post("/sentiment")
async def createSentiment(sentimentCreate: MessageSentimentCreate,
                          db: Session = Depends(get_db)):

    watsonResp = await watson.getSentiment(sentimentCreate.content)

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

    insertMessageSentiment(db, messageSentiment)

    print(watsonResp)
