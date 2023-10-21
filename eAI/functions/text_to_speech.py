from google.cloud import speech
from google.oauth2 import service_account
import io

credientials = service_account.Credentials.from_service_account_file("key.json")
client = speech.SpeechClient(credentials=credientials)
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=44100,
    enable_automatic_punctuation=True,
    language_code='en-US',
)


def convert_audio_to_text(audio_file_path):
    try:
        with io.open(audio_file_path, 'rb') as audio:
            audio_mp3 = audio.read()
        audio_file = speech.RecognitionAudio(content=audio_mp3)

        response = client.recognize(
            config=config,
            audio=audio_file
        )
        return response
    except Exception as e:
        print(e)
