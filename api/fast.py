from fastapi import FastAPI
from tensorflow.keras import models
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
import numpy as np
from pydantic import BaseModel
from helpers import image_from_dict, image_to_dict
from road_detector.unet import GiveMeUnet
app = FastAPI()
LOCAL_Weights = '/Users/loulou/code/annabalaguy/API_road_detector/road_detector/WEIGHTS_Vincent_Jaccard_Crossentropy.h5'

unet = GiveMeUnet()
unet.load_weights(LOCAL_Weights)

#Upload de l'Image par l'utilisateur

class Item(BaseModel):
    image: str
    size : int
    height: int
    width: int
    channel: int

@app.get("/")
def test():
    return {"status": "OK"}

@app.post("/predict")
async def prediction(item:Item):
    #Conversion de l'image en nparray
    img = image_from_dict(item, dtype='float32')

    # Preproc + predict à cet endroit
    #img=pad_sequences(img)

    #Prediction de l'image

    predict_img=unet.predict(img)

    #Conversion du nparray en image str lisible pour l'API
    image_predite = image_to_dict(predict_img, dtype='float16')

    # TO DO: Option to convert tf to np -> prediction.numpy()
    # TO DO: Option to unscale *255 -> prediction * 255

    return image_predite


@app.get("/test")
def home():
    return {"Bonjour à tous"}


@app.get("/")
def index():
    return {"Bonjour à tous"}