from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gtts import gTTS
import gtts.lang
import os
import base64
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_langs():
    langs = gtts.lang.tts_langs()
    #to array key and value
    langs = [[k, v] for k, v in langs.items()]
    return langs

def get_tts(text, lang):
    tts = gTTS(text=text, lang=lang)
    #save to directory /tmp
    tts.save("/tmp/tts.mp3")
    

class Msg(BaseModel):
    msg: str

class TTS(BaseModel):
    text: str
    lang: str

@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to FastAPI!"}


@app.get("/path")
async def demo_get():
    return {"message": "This is /path endpoint, use a post request to transform the text to uppercase"}


@app.post("/path")
async def demo_post(inp: Msg):
    return {"message": inp.msg.upper()}


@app.get("/path/{path_id}")
async def demo_get_path_id(path_id: int):
    return {"message": f"This is /path/{path_id} endpoint, use post request to retrieve result"}

@app.get("/langs")
async def langs():
    return {"langs": get_langs()}

@app.post("/tts")
async def tts(tts: TTS):
    get_tts(tts.text, tts.lang)
    with open("/tmp/tts.mp3", "rb") as f:
        data = f.read()
    return {"audio": base64.b64encode(data).decode(), "mime": "audio/mpeg" , "ext": "mp3" , "lang": tts.lang}
