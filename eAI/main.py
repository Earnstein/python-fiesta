# from fastapi import FastAPI, File, UploadFile, HTTPException
# from fastapi.responses import  StreamingResponse
# from fastapi.middleware.cors import CORSMiddleware
# from decouple import config
# from functions.openai_requests import convert_audio_to_text
# import openai
#
# app = FastAPI()
# # Custom functions import
#
# # Cors origins
# origins = [
#     "http://localhost:5137",
#     "http://localhost:5174",
#     "http://localhost:4137",
#     "http://localhost:4174",
#     "http://localhost:3000",
# ]
#
# # Cors middlewares
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )
#
#
# # check
# @app.get("/")
# async def root():
#     return {"message": "Hello world"}
#
#
# @app.get("/health")
# async def check_health():
#     return {"message": "Check Health"}
#
#
# @app.get("/get-audio")
# async def http_get_audio():
#     audio_text = convert_audio_to_text("myvoice.mp3")
#     print(audio_text)
#     return "done"
#

from functions.text_to_speech import convert_audio_to_text

result = convert_audio_to_text("myvoice.mp3")
print(result)