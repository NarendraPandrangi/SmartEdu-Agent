import os
import json
import re
from dotenv import load_dotenv
from typing import Optional, List
from models import ContentOutput, ReviewFeedback, ContentRequest
from krutrim_cloud import KrutrimCloud

load_dotenv()

model_name = "Krutrim-spectre-v2"

def extract_or_construct_json(text: str) -> str:
    # Try basic JSON extraction first
    cleaned_text = re.sub(r'```json\s*|\s*```', '', text)
    start = cleaned_text.find('{')
    end = cleaned_text.rfind('}')
    
    if start != -1 and end != -1 and end > start:
        candidate = cleaned_text[start:end+1]
        try:
            json.loads(candidate)
            return candidate
        except json.JSONDecodeError:
            pass # Continue to fallback

    # Fallback: Construct JSON from text
    # This is a heuristic parser for the failing model output
    explanation = "Generated content"
    mcqs = []
    
    lines = text.split('\n')
    current_mcq = None
    capture_explanation = True
    explanation_lines = []

    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Check for Answer line FIRST
        ans_match = re.search(r'Answer:\s*([A-Da-d])', line, re.IGNORECASE)
        if ans_match:
            if current_mcq:
                current_mcq["answer"] = ans_match.group(1).upper() + ")"
            continue

        # Check for Question Start pattern
        q_match = re.match(r'^(?:Question\s*)?(\d+)[\.\)\:\-]?\s+(.*)', line, re.IGNORECASE)
        
        # Detect start of MCQs section (header)
        if capture_explanation:
            lower_line = line.lower()
            # Explicit separator from strict prompt
            if "### mcqs" in lower_line:
                capture_explanation = False
                continue
            
            # Natural language header fallback
            if "multiple choice questions" in lower_line or "mcqs" in lower_line or "assessment" in lower_line:
                # Be careful not to trigger on "In this lesson about multiple choice questions..."
                # Headers are usually short.
                if len(line) < 50:
                    capture_explanation = False
                    if not q_match:
                        continue
            
            # Heuristic: Start of a question often looks like "1. What...?"
            if q_match:
                # If the line ends with a question mark, it's very likely a question
                if line.endswith('?'):
                     capture_explanation = False
                # Or if it explicitly starts with "Question"
                elif line.lower().startswith("question"):
                     capture_explanation = False

        if capture_explanation:
            explanation_lines.append(line)
        else:
            # Parse MCQs Questions
            if q_match:
                if current_mcq:
                    mcqs.append(current_mcq)
                
                q_text = q_match.group(2).strip()
                if not q_text:
                    q_text = "Question " + q_match.group(1)
                
                current_mcq = {"question": q_text, "options": [], "answer": "A)"} 
                continue 
            
            # Check for options
            if current_mcq:
                # Normalize prefix to "A) "
                opt_match = re.match(r'^[\-]?\s*([A-Da-d])([\.\)\-])\s*(.*)', line)
                if opt_match:
                    letter = opt_match.group(1).upper()
                    content = opt_match.group(3)
                    current_mcq["options"].append(f"{letter}) {content}")
                elif line.startswith('-'):
                     current_count = len(current_mcq["options"])
                     letters = ['A', 'B', 'C', 'D']
                     if current_count < 4:
                        prefix = letters[current_count] + ") "
                        current_mcq["options"].append(prefix + line.lstrip('- ').strip())
                     else:
                        current_mcq["options"].append(line)
                else:
                    if len(current_mcq["options"]) == 0:
                        if current_mcq["question"].lower().startswith("question") and len(current_mcq["question"]) < 15:
                             current_mcq["question"] = line 
                        else:
                             current_mcq["question"] += " " + line
                    elif len(current_mcq["options"]) < 4:
                        current_count = len(current_mcq["options"])
                        letters = ['A', 'B', 'C', 'D']
                        prefix = letters[current_count] + ") "
                        current_mcq["options"].append(prefix + line.strip())

    if current_mcq:
        mcqs.append(current_mcq)

    # Validate MCQs
    if len(mcqs) == 0:
        # Fallback: If no MCQs found, maybe the model didn't label them perfectly.
        # But for now, we return empty so the user knows it failed, or we could try to re-parse explanation?
        # Let's trust the "Failed to parse" so we can debug.
        pass
        
    return json.dumps({
        "explanation": " ".join(explanation_lines).replace("Explanation:", "").strip(),
        "mcqs": mcqs
    })

def extract_review_json(text: str) -> str:
    cleaned_text = re.sub(r'```json\s*|\s*```', '', text)
    start = cleaned_text.find('{')
    end = cleaned_text.rfind('}')
    if start != -1 and end != -1 and end > start:
         return cleaned_text[start:end+1]
    
    # Fallback for reviewer
    status = "fail"
    if "pass" in text.lower() and "fail" not in text.lower():
        status = "pass"
    
    return json.dumps({
        "status": status,
        "feedback": [text.strip()]
    })

class GeneratorAgent:
    def __init__(self):
        api_key = os.getenv("KUTRIM_API_KEY")
        if not api_key:
            raise ValueError("KUTRIM_API_KEY not found in .env")
        self.client = KrutrimCloud(api_key=api_key)

    def generate(self, request: ContentRequest, feedback: Optional[List[str]] = None) -> ContentOutput:
        prompt = f"""
        You are an educational content generator API.
        Target Audience: Grade {request.grade}
        Topic: {request.topic}
        
        Structure your response exactly like this:
        
        Explanation:
        [Write a concise explanation here]
        
        ### MCQs
        
        1. [Question Text]
        A) [Option 1]
        B) [Option 2]
        C) [Option 3]
        D) [Option 4]
        Answer: [Correct Option, e.g. A)]
        
        2. [Question Text]
        ...
        
        Generate 3 questions. Ensure you include the '### MCQs' separator and the 'Answer:' line for each.
        """
        
        if feedback:
            prompt += f"\n\nRefinement Request based on previous feedback:\n{json.dumps(feedback)}"
        
        try:
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
                temperature=0.5
            )
            
            content_text = response.choices[0].message.content.strip()
            print(f"Generator Raw Output: {content_text}")
            
            # Log to file for debug
            try:
                with open("debug_response.txt", "w", encoding="utf-8") as f:
                    f.write(content_text)
            except:
                pass

            json_text = extract_or_construct_json(content_text)
            return ContentOutput.model_validate_json(json_text)
        except Exception as e:
            print(f"Error in GeneratorAgent: {e}")
            raise ValueError(f"Generator failed: {str(e)}")

class ReviewerAgent:
    def __init__(self):
        api_key = os.getenv("KUTRIM_API_KEY")
        if not api_key:
             raise ValueError("KUTRIM_API_KEY not found in .env")
        self.client = KrutrimCloud(api_key=api_key)

    def review(self, content: ContentOutput, request: ContentRequest) -> ReviewFeedback:
        prompt = f"""
        You are an educational content reviewer API.
        Target Audience: Grade {request.grade}
        Topic: {request.topic}
        
        Evaluate the following content:
        {content.model_dump_json()}
        
        Criteria:
        1. Age appropriateness
        2. Correctness
        3. Clarity
        4. Completeness (Are there 3 MCQs?)
        
        If MCQs are missing or fewer than 3, you MUST FAIL.
        
        Output Structure (JSON only):
        {{
            "status": "pass", 
            "feedback": []
        }}
        OR if there are issues:
        {{
            "status": "fail",
            "feedback": ["issue 1", "issue 2"]
        }}
        """
        
        try:
             response = self.client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.3
            )
             
             content_text = response.choices[0].message.content.strip()
             print(f"Reviewer Raw Output: {content_text}")
             
             json_text = extract_review_json(content_text)
             return ReviewFeedback.model_validate_json(json_text)
        except Exception as e:
             print(f"Error in ReviewerAgent: {e}")
             raise ValueError(f"Reviewer failed: {str(e)}")
