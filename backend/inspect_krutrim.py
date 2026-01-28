from krutrim_cloud import KrutrimCloud
import sys

try:
    client = KrutrimCloud(api_key="example")
    # Redirect stdout to avoid interference
    sys.stderr.write(f"BASE_URL_FOUND: {client.base_url}\n")
except Exception as e:
    sys.stderr.write(f"ERROR: {e}\n")
