import openai
from decouple import config

openai.organization = config("OPENAI_ORG")
openai.api_key = config("OPENAI_KEY")

#Audio conversion


def convert_audio_to_text(audio_file_path):
    try:
        with open(audio_file_path, 'rb') as audio_file:
            transcription = openai.Audio.transcribe("whisper-1", audio_file)
        return transcription['text']
    except Exception as e:
        print(e)
