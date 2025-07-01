from uuid import uuid4
from fastapi import FastAPI
from bot.models.request import ChatbotRequestModel
from bot.models.response import ChatbotResponseModel
from bot.predicting import PredictBot

# --- FastAPI App ---
app = FastAPI()


# --- Endpoints ---
@app.get("/isAlive")
def is_alive():
    return "true"


@app.post("/predictedLabel/")
def predict_label(req: ChatbotRequestModel) -> ChatbotResponseModel:

    bot = PredictBot()
    msg = bot.get_predicted_label(message=req.text)

    return ChatbotResponseModel(text=msg, checkpointer_id=str(uuid4()))


@app.post("/predictedMessage/")
def predict_message(req: ChatbotRequestModel) -> ChatbotResponseModel:

    bot = PredictBot()
    msg = bot.predicted_msg(message=req.text)

    return ChatbotResponseModel(text=msg, checkpointer_id=str(uuid4()))
