from dotenv import load_dotenv
load_dotenv()
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize,generate_title
from core.extractor import extract_action_items,extract_decisions_items,extract_questions
import os

print("KEY LOADED:")
print("CWD:",os.getcwd())

source="https://www.youtube.com/watch?v=52t241OQ7Ec"
language="english"

chunks=process_input(source)

transcript=transcribe_all(chunks,language=language)
print("\n"+"="*60)
print("TRANSCRIPT")
print("="*60)
print(transcript[:500]+"..." if len(transcript) >500 else transcript)

title = generate_title(transcript)
summary= summarize(transcript)

print(f"TITLE:{title}")
print("="*60)
print("SUMMARY")

print("="*60)
print(summary)

action=extract_action_items(transcript)
decisions= extract_decisions_items(transcript)
questions=extract_questions(transcript)
print("="*60)
print("ACTIONS")
print(action)
print("="*60)
print("DECISIONS")
print(decisions)
print("="*60)
print("QUESTIONS")
print(questions)
print("="*60)