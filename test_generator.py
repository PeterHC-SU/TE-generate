import asyncio
import os
from dotenv import load_dotenv
from geminimodel import GeminiTestCaseGenerator
import json

load_dotenv()

async def test_generate_test_cases():
    # init the generator and learning system
    api_key = "AIzaSyAEoBo5ur2iuS55pZIQb8D50XQI0PdXoT0"
    if not api_key:
        raise ValueError("Please set the GEMINI_API_KEY environment variable")
        
    generator = GeminiTestCaseGenerator(api_key=api_key)
    
    # test URLs
    prd_url = "https://carousell.atlassian.net/wiki/spaces/UAC/pages/2741403649/PRD+Offer+to+Likers"
    figma_url = "https://www.figma.com/design/QQb1FVxgvmUN79gjavh31u/Offer-to-likers?node-id=1-8&t=Zmq4W3jlAglC1dyd-1"
    
    try:
        # Generate Test Cases
        print("\n=== Generate Test Cases ===\n")
        initial_result = await generator.generate_test_cases(prd_url, figma_url)
        print("initial test cases:")
        print(initial_result["test_cases"])

    except Exception as e:
        print(f"error: {str(e)}")

if __name__ == "__main__":
    # execute test
    asyncio.run(test_generate_test_cases())