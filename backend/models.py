from pydantic import BaseModel
from typing import List, Optional, Literal

class MCQ(BaseModel):
    question: str
    options: List[str]
    answer: str

class ContentOutput(BaseModel):
    explanation: str
    mcqs: List[MCQ]

class ReviewFeedback(BaseModel):
    status: Literal["pass", "fail"]
    feedback: List[str]

class ContentRequest(BaseModel):
    grade: int
    topic: str

class PipelineResponse(BaseModel):
    original_content: Optional[ContentOutput] = None
    feedback: Optional[ReviewFeedback] = None
    refined_content: Optional[ContentOutput] = None
    final_status: Literal["pass", "fail"]
    trace_id: str
