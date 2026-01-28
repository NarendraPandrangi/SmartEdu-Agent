import os
from dotenv import load_dotenv

load_dotenv()

print("Environment variables check:")
print(f"KUTRIM_API_KEY exists: {bool(os.getenv('KUTRIM_API_KEY'))}")
print(f"KUTRIM_API_KEY value: {os.getenv('KUTRIM_API_KEY', 'NOT FOUND')[:10]}...")
print(f"All env vars: {list(os.environ.keys())}")
