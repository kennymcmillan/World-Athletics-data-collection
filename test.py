

import pydantic
print(f"Pydantic version: {pydantic.__version__}")

import httpx
print(f"HTTPX version: {httpx.__version__}")

import websockets
print(f"Websockets version: {websockets.__version__}")

# test_import.py
try:
    import worldathletics
    print("Import successful!")
except Exception as e:
    print(f"Error during import: {e}")
