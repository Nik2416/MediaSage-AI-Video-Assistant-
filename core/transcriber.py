import whisper
import os
import requests


WHISPER_MODEL= os.getenv("WHISPER_MODEL","small")

_model =None

from dotenv import load_dotenv

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

SARVAM_STT_URL = "https://api.sarvam.ai/speech-to-text"
SARVAM_MODEL = "saaras:v4"

def load_model():

  global _model

  if _model is None :
    print(f"Loading model...")
    _model= whisper.load_model(WHISPER_MODEL)
    print("Whisper model loaded successfully")

  return _model

def transcribe_chunk_whisper(chunk_path):

  model=load_model()

  result = model.transcribe(chunk_path,task="transcribe")

  return result['text']

  
def transcribe_chunk_sarvam(chunk_path):

    if not SARVAM_API_KEY:
        raise RuntimeError("SARVAM_API_KEY is not loaded. Check your .env file.")

    headers = {
        "api-subscription-key": SARVAM_API_KEY
    }

    with open(chunk_path, "rb") as f:

        files = {
            "file": (os.path.basename(chunk_path), f, "audio/wav")
        }

        data = {
            "model": SARVAM_MODEL,
            "mode": "translate"
        }

        response = requests.post(
            SARVAM_STT_URL,
            headers=headers,
            files=files,
            data=data,
            timeout=120
        )

    if not response.ok:
        raise RuntimeError(
            f"Sarvam API Error: {response.status_code} - {response.text}"
        )

    return response.json().get("transcript", "")



  


def transcribe_chunk(chunk_path,language="english"):
   if language.lower()=="hinglish":
      return transcribe_chunk_sarvam(chunk_path)
   return transcribe_chunk_whisper(chunk_path)



def transcribe_all(chunks,language="english"):

  full_transcript=""


  engine="Sarvam AI" if language.lower()=="hinglish" else "whisper"
  print(f"Using {engine} for transcription.")

  for i,chunk in enumerate(chunks):
     print(f"Transcribing chunk{i+1}")
     text= transcribe_chunk(chunk,language=language)

     full_transcript+= text + " "

  print("Transcription completed.")

  return full_transcript.strip()


   
