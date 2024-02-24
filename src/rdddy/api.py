"""rdddy REST API."""
import logging
import coloredlogs

import dspy
from pydantic import BaseModel

from rdddy.signatures.code_interview_solver import CodeInterviewSolver

from fastapi import FastAPI

app = FastAPI()

lm = dspy.OpenAI(max_tokens=1000)
dspy.settings.configure(lm=lm)


class TranscriptData(BaseModel):
    transcript: str


@app.post("/receive_transcript")
async def process_transcript(data: TranscriptData):
    transcript = data.transcript
    # Process your transcript here
    cot = (
        dspy.ChainOfThought(CodeInterviewSolver)
        .forward(problem_statement=transcript)
        .detailed_code_solution
    )
    print(cot)
    return {"message": f"Transcript received: {cot}"}
