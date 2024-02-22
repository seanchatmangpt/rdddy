"""rdddy REST API."""

import logging

import dspy
from pydantic import BaseModel

import coloredlogs
from fastapi import FastAPI

from rdddy.signatures.code_interview_solver import CodeInterviewSolver

app = FastAPI()

lm = dspy.OpenAI(max_tokens=1000)
dspy.settings.configure(lm=lm)

@app.on_event("startup")
def startup_event() -> None:
    """Run API startup events."""
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    # Add coloredlogs' coloured StreamHandler to the root logger.
    coloredlogs.install()


@app.get("/")
def read_root() -> str:
    """Read root."""
    return "Hello world"


from fastapi import FastAPI, Request

app = FastAPI()

class TranscriptData(BaseModel):
    transcript: str

@app.post("/receive_transcript")
async def process_transcript(data: TranscriptData):
    transcript = data.transcript
    # Process your transcript here
    cot = dspy.ChainOfThought(CodeInterviewSolver).forward(problem_statement=transcript).detailed_code_solution
    print(cot)
    return {"message": f"Transcript received: {cot}"}
