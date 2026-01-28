from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from models import ContentRequest, PipelineResponse, ContentOutput
from agents import GeneratorAgent, ReviewerAgent
import uuid

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev simplicity, allow all. In prod, specify localhost:5173
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

generator = GeneratorAgent()
reviewer = ReviewerAgent()

@app.post("/api/generate-content", response_model=PipelineResponse)
async def generate_content_pipeline(request: ContentRequest):
    trace_id = str(uuid.uuid4())
    
    # 1. Generate
    try:
        draft = generator.generate(request)
    except Exception as e:
        import traceback
        error_detail = f"Generator failed: {str(e)}\nTraceback: {traceback.format_exc()}"
        print(error_detail)  # This will show in Vercel logs
        raise HTTPException(status_code=500, detail=f"Generator failed: {str(e)}")

    # 2. Review
    try:
        review_result = reviewer.review(draft, request)
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Reviewer failed: {str(e)}")
    
    refined_content = None
    final_status = review_result.status

    # 3. Refine (if needed)
    if review_result.status == "fail":
        try:
             refined_content = generator.generate(request, feedback=review_result.feedback)
             # Optional: Review again? PDF says "Limit to one refinement pass", implies we just accept it or maybe mark it. 
             # We will just return it as the final result of this pipeline pass.
             # Ideally we might review the refinement, but for "Lightweight" logic, we just output it.
        except Exception as e:
             # If refinement fails, we stick with original but mark failed? 
             # Or raise error. Let's log and keep original as 'original' but 'refined' is None
             print(f"Refinement failed: {e}")
    
    return PipelineResponse(
        original_content=draft,
        feedback=review_result,
        refined_content=refined_content,
        final_status=final_status,
        trace_id=trace_id
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
