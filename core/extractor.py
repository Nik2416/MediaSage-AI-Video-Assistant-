#Actionable items, decisions ,Questions
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
import os


def get_llm():
  return ChatGroq(model="openai/gpt-oss-20b",groq_api_key=os.getenv("GROQ_API_KEY"),temperature=0.2)


def build_chain(system_prompt):
  llm=get_llm()

  
  return ( 
    RunnablePassthrough()|RunnableLambda(lambda x :{"text":x})|ChatPromptTemplate.from_messages(
      [
    ("system",system_prompt),
    ("human","{text}"),
    ])|llm
    |StrOutputParser()
  )


def extract_action_items(transcript):
  chain=build_chain(
   """
You are an expert meeting action-item extractor.

Your task is to identify only tasks that need to be
performed after or during the meeting.

An action item must represent an actual commitment,
assignment, or clearly agreed future task.

For each item provide:
- Task description
- Owner
- Deadline

Rules:
1. Do not include decisions unless they also create
   a separate task.
2. Do not include unanswered questions.
3. Do not treat casual suggestions as commitments.
4. If the owner is unknown, write Not Specified.
5. If the deadline is unknown, write Not Specified.
6. Do not invent information.
7. Avoid duplicate action items.

If no action items exist, return exactly:
No action items found.

Format as a numbered list.
"""

  )
  return chain.invoke(transcript)

def extract_decisions_items(transcript):
  chain=build_chain(
    """
You are an expert meeting decision analyst.

Extract ONLY final decisions explicitly agreed upon
or confirmed during the meeting.

A decision is a choice, agreement, or conclusion
that the participants have reached.

Rules:
1. Do not include tasks or assignments.
2. Do not include suggestions that were not accepted.
3. Do not include unresolved questions.
4. Do not convert future intentions into decisions
   unless an actual choice was made.
5. Avoid duplicate decisions.
6. Do not invent decisions.

If no decisions exist, return exactly:
No key decisions found.

Format as a numbered list.
"""

  )
  return chain.invoke(transcript)

def extract_questions(trancript):
  chain= build_chain(
    """
You are an expert meeting analyst.

Extract ONLY unresolved questions and topics
that require further clarification or discussion.

Rules:
1. Include questions that were asked but not answered.
2. Include issues explicitly left pending.
3. Do not include questions that were already resolved.
4. Do not include ordinary action items.
5. Do not include final decisions.
6. Do not invent questions.
7. Avoid duplicates.

If no unresolved questions exist, return exactly:
No open questions found.

Format as a numbered list.
"""
  )
  return chain.invoke(trancript)

