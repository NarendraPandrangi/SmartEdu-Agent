from agents import GeneratorAgent
from models import ContentRequest
import os

try:
    print("Testing GeneratorAgent directly...")
    agent = GeneratorAgent()
    req = ContentRequest(grade=5, topic="Planets")
    print(f"Request: {req}")
    res = agent.generate(req)
    print("Success!")
    print(res.model_dump_json(indent=2))
except Exception as e:
    print("Failed!")
    print(e)
