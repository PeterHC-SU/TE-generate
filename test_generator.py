import asyncio
import os
# from dotenv import load_dotenv
from geminimodel import GeminiTestCaseGenerator
import json


API_KEY = "YOUR_KEY"
PRD_URL = "PRD_URL"
FIGMA_URL = "FIGMA_URL"
    

async def test_generate_test_cases():
    # init the generator and learning system

    if not API_KEY:
        raise ValueError("Please set the GEMINI_API_KEY environment variable")
        
    generator = GeminiTestCaseGenerator(api_key=API_KEY)
    
    # test URLs
    
    try:
        # Generate Test Cases
        print("\n=== Generate Test Cases ===\n")
        initial_result = await generator.generate_test_cases(PRD_URL, FIGMA_URL)
        print("initial test cases:")
        print(initial_result["test_cases"])

    except Exception as e:
        print(f"error: {str(e)}")

if __name__ == "__main__":
    # execute test
    asyncio.run(test_generate_test_cases())
