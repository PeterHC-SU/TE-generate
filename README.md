# Gemini Gherkin Test Case Generator

This project uses the Gemini API to automatically generate Gherkin-style BDD test cases based on a PRD (Product Requirements Document) and Figma UI design.

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```
### 2. Run the Generator
```
python test_generator.py
```
## ⚙️ Configuration
Before running the script, open test_generator.py and set the following variables:

GEMINI_API_KEY: Your Gemini API key.

PRD_URL: The URL of the product requirements document you want to test.

FIGMA_URL: The URL of the corresponding Figma UI design.

Example:
```
GEMINI_API_KEY = "your-gemini-api-key"
PRD_URL = "https://your.prd.url"
FIGMA_URL = "https://your.figma.file.url"
```
