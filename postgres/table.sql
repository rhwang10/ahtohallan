CREATE TABLE message_sentiments (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    discord_id integer NOT NULL,
    content text NOT NULL,
    document_sentiment double precision NOT NULL,
    document_sentiment_label text NOT NULL,
    document_emotion_sadness double precision NOT NULL,
    document_emotion_joy double precision NOT NULL,
    document_emotion_fear double precision NOT NULL,
    document_emotion_disgust double precision NOT NULL,
    document_emotion_anger double precision NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
);

CREATE INDEX idx_discord_id ON message_sentiments(discord_id);
