import os
import json
import requests
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from datetime import datetime

MODEL_ID = "gemini-2.0-flash"  # Default model

class GeminiTestCaseGenerator:
    """Use Gemini AI model to generate Gherkin test cases"""
    
    def __init__(self, api_key: str, model_name: str = MODEL_ID):
        """Initialize Gemini test case generator
        
        Args:
            api_key: Gemini API key
            model_name: Gemini model name
        """
        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
        self.system_prompt = self._load_system_prompt()
        
    def _load_system_prompt(self) -> str:
        """Load system prompt template"""
        return """
        # You are a professional QA test automation expert specializing in creating Gherkin-style test cases.

        # Your task is to analyze the Product Requirements Document (PRD) and UI designs to generate comprehensive BDD test cases.

        # Please follow these guidelines:
        # 1. Properly create the Feature, Background, and Scenario sections
        # 2. Cover all major user flows described in the requirements
        # 3. Include both positive and negative test scenarios
        # 4. Reference the exact UI element names from the design
        # 5. Clearly specify preconditions, actions, and expected outcomes
        # 6. Include data validation test cases where applicable
        # 7. Consider boundary conditions and error-handling scenarios
        # 8. Use correct Gherkin syntax and indentation
        # 9. Ensure test cases are repeatable
        # 10. Include sufficient verification points
        # 11. Account for various combinations of business logic
        # 12. Be mindful of data dependencies

        # The output should contain only valid Gherkin syntax, without any explanations or markdown.
        """
    
    def _load_learned_patterns(self) -> List[Dict]:
        """Load learned test patterns from file or use defaults"""
        try:
            if os.path.exists('learned_patterns.json'):
                with open('learned_patterns.json', 'r') as f:
                    return json.load(f)
            else:
                return [
                    {
                        "pattern_type": "validation",
                        "description": "Include explicit validation for user inputs with specific error messages",
                        "examples": ["Then I should see error message \"Discount must be at least 5%\""]
                    },
                    {
                        "pattern_type": "ui_interaction",
                        "description": "Specify exact UI element names and locations",
                        "examples": ["When I tap on the \"Offer to Likers\" button in the listing actions section"]
                    }
                ]
        except Exception as e:
            print(f"Error loading learned patterns: {e}")
            return []
    
    async def generate_test_cases(self, prd_url: str, figma_url: str) -> Dict:
        """Generate test cases from PRD and Figma URL
        
        Args:
            prd_url: PRD document URL
            figma_url: Figma design URL
            
        Returns:
            Generated test cases and metadata
        """
        # Get PRD content
        prd_content = await self._fetch_document_content(prd_url)
        
        # Get Figma design content and screenshots
        figma_data = await self._fetch_figma_content(figma_url)
        
        # Generate test cases with Gemini
        test_cases = await self._generate_with_gemini(prd_content, figma_data)
        
        # Post-process results to ensure correct format
        formatted_cases = self._post_process_test_cases(test_cases)
        
        return {
            "status": "success",
            "test_cases": formatted_cases,
            "metadata": {
                "prd_url": prd_url,
                "figma_url": figma_url,
                "generation_timestamp": self._get_current_timestamp(),
                "model_version": MODEL_ID
            }
        }
    
    async def _fetch_document_content(self, doc_url: str) -> str:
        """Get document content from URL
        
        Args:
            doc_url: Document URL (Atlassian, Google Docs, etc.)
            
        Returns:
            Document text content
        """
        # Parse URL type
        if "atlassian.net" in doc_url:
            return await self._fetch_atlassian_content(doc_url)
        elif "docs.google.com" in doc_url:
            return await self._fetch_google_docs_content(doc_url)
        else:
            # Try to get content directly
            try:
                response = requests.get(doc_url)
                response.raise_for_status()
                return response.text
            except Exception as e:
                print(f"Error fetching document: {e}")
                return f"Could not fetch document from {doc_url}. Please ensure the URL is accessible."
    
    async def _fetch_atlassian_content(self, atlassian_url: str) -> str:
        """Get content from Atlassian (Confluence/JIRA)"""
        # In actual implementation, this will use Atlassian API
        try:
            # Parse URL to get page ID
            page_id = atlassian_url.split("pages/")[1].split("/")[0]
            
            # Example data
            return page_id
            
        except Exception as e:
            print(f"Error fetching Atlassian content: {e}")
            return "Could not fetch Atlassian document. Please ensure the URL is correct and accessible."
    
    async def _fetch_google_docs_content(self, gdocs_url: str) -> str:
        """Get content from Google Docs"""
        # In actual implementation, this will use Google Docs API
        return "Google Docs integration requires OAuth2 authorization. Please use Atlassian or direct text input."
    
    async def _fetch_figma_content(self, figma_url: str) -> Dict:
        """Get design content and screenshots from Figma
        
        Args:
            figma_url: Figma design URL
            
        Returns:
            Dictionary containing design information and screenshots
        """
        try:
            # Parse Figma URL to get file and node ID
            file_key = figma_url.split("/")[4]
            node_id = figma_url.split("node-id=")[1].split("&")[0] if "node-id=" in figma_url else None
            
            return {
                "file_key": file_key,
                "node_id": node_id,
                "design_info": self._get_mock_design_info(),
                "screenshots": []
            }
        except Exception as e:
            print(f"Error fetching Figma content: {e}")
            return {
                "file_key": None,
                "node_id": None,
                "design_info": "Could not parse Figma URL. Please ensure it's correct.",
                "screenshots": []
            }
    
    def _get_mock_design_info(self) -> str:
        """Get mock design information for development purposes"""
        return """
        UI Elements:
        
        1. "Offer to Likers" button - Located in listing actions menu
        2. Offer Modal Dialog - Contains offer creation form
        3. Recipient Selection - Radio buttons: "All Likers (5)" and "Select Likers"
        4. Liker Selection List - Checkbox list of likers (when "Select Likers" is chosen)
        5. "Offer Price" input field - Numeric input for offer price
        6. Discount Percentage Display - Shows calculated discount from original price
        7. "Send Offer" button - Primary button to send the offer
        8. "Cancel" button - Secondary button to dismiss modal
        9. Error Message Area - Displays validation errors
        10. Success Confirmation - Shows after successful offer creation
        
        Buyer Side:
        11. Offer Notification - Alert showing new offer received
        12. Offer Details View - Shows original price, offer price, expiry timer
        13. "Accept Offer" button - To accept the discounted price
        14. "Decline" button - To reject the offer
        """
    
    async def _generate_with_gemini(self, prd_content: str, figma_data: Dict) -> str:
        """Generate test cases with Gemini
        
        Args:
            prd_content: PRD document content
            figma_data: Figma design data
            
        Returns:
            Generated Gherkin test cases
        """
        # Build prompt
        prompt = self._build_prompt(prd_content, figma_data)
        
        # Call Gemini to generate content
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating with Gemini: {e}")
            return "Error generating test cases. Please try again."
    
    def _build_prompt(self, prd_content: str, figma_data: Dict) -> str:
        """Build prompt for AI generation
        
        Args:
            prd_content: PRD content
            figma_data: Figma design data
            
        Returns:
            Complete prompt
        """
        design_info = figma_data.get("design_info", "No design information available")
        
        prompt = f"""
        {self.system_prompt}
        
        # PRD CONTENT:
        {prd_content}
        
        # UI DESIGN INFORMATION:
        {design_info}
        
        Generate comprehensive Gherkin test cases for the feature described above.
        Include Feature, Background, and multiple Scenarios that cover both happy paths and edge cases.
        """
        
        return prompt
    
    def _post_process_test_cases(self, raw_output: str) -> str:
        """Post-process test cases to ensure correct format
        
        Args:
            raw_output: Raw output generated by the model
            
        Returns:
            Formatted Gherkin test cases
        """
        # Clean output
        cleaned_output = raw_output.strip()
        
        # Find Gherkin start
        feature_index = cleaned_output.find("Feature:")
        if feature_index >= 0:
            cleaned_output = cleaned_output[feature_index:]
            
        # Ensure no extra content
        # Find the last Scenario or Scenario Outline
        last_scenario = max(
            cleaned_output.rfind("Scenario:"),
            cleaned_output.rfind("Scenario Outline:")
        )
        
        if last_scenario >= 0:
            # Find the next possible non-Gherkin content
            potential_endings = []
            for marker in ["Note:", "Notes:", "Comment:", "Comments:", "Explanation:", "#"]:
                pos = cleaned_output.find(marker, last_scenario)
                if pos >= 0:
                    potential_endings.append(pos)
                    
            if potential_endings:
                end_pos = min(potential_endings)
                cleaned_output = cleaned_output[:end_pos].strip()
                
        return cleaned_output
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.now().isoformat()
    