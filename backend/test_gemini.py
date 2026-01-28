from agents import GeneratorAgent
from models import ContentRequest
import os

try:
    print("Testing GeneratorAgent...")
    agent = GeneratorAgent()
    req = ContentRequest(grade=5, topic="Photosynthesis")
    print("Sending request...")
    res = agent.generate(req)
    print("Success!")
    print(res)
except Exception as e:
    print("Failed!")
    print(e)
