import os
import json
import re
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from transformers import pipeline
import requests
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware 
import logging

# Configure logging (do this ONCE at the beginning of your file)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Create a logger instance (this was missing)
logger = logging.getLogger(__name__)  # __name__ is good practice

app = FastAPI(title="Sentiment Analysis API")

# CORS Configuration (Most Robust)
origins = [
    "http://localhost:3000",
    "http://localhost:3001"  # Your React app's origin (ADD MORE IF NEEDED)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Important if you use cookies or sessions
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Environment Variables fro Groq and setting up Groq
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")  # Set this in your environment!
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable must be set.")

client = Groq(api_key=GROQ_API_KEY)  

# Custom model loading
try:
    hf_model = pipeline("sentiment-analysis", model="pmranu/imdb-fine-tuned-sentiment-analyzer")
    print("Hugging Face model loaded.")
except Exception as e:
    print(f"Error loading Hugging Face model: {e}")
    hf_model = None

# Data Validation (Pydantic):
class AnalyzeRequest(BaseModel):
    text: str 
    model: str


# 5. Model Availability Check (Dependency Injection):
def check_model_availability(model_name: str):
    if model_name == "custom" and hf_model is None:
        raise HTTPException(status_code=500, detail="Custom model not available.")
    elif model_name == "llama" and not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="Llama model not available (Groq API key missing).")
    return model_name

# 6. Llama Prompt (Step 9 - Improved):
LLAMA_PROMPT = """ You are a sentiment analysis expert. 
Carefully analyze the sentiment of the following text and provide your response in JSON format as shown below.  
The sentiment should be either "positive" or "negative".  
The confidence should be a score between 0.0 and 1.0, indicating your confidence in the sentiment classification.

Text: {text}

JSON Response:
```json
{{
  "sentiment": "positive" or "negative",
  "confidence": 0.0 - 1.0
}}

Give just json as response!"""
@app.post("/analyze/")
async def analyze_text(request: AnalyzeRequest):
    try:
        text = request.text
        model_choice = request.model

        if model_choice == "custom":
            if hf_model is None:  # Handle the case where model loading failed
                raise HTTPException(status_code=500, detail="Custom model not available.")
            model = hf_model
            try:
                result = model(text)[0]
                sentiment = result["label"]
                if sentiment == "LABEL_0":
                    sentiment = "negative"
                elif sentiment == "LABEL_1":
                    sentiment = "positive"
                confidence = result["score"]
            except Exception as e:
                print(f"Error during Hugging Face analysis: {e}")
                raise HTTPException(status_code=500, detail="Error analyzing text.")

        elif model_choice == "llama":
            try:
                response = client.chat.completions.create(
                    messages=[{
                        "role": "user",
                        "content": LLAMA_PROMPT.format(text=text) # Use the improved prompt
                    }],
                    model="llama-3.3-70b-versatile"  # Or another suitable Llama model
                )

                json_response_str = response.choices[0].message.content

                # Extract JSON using a regular expression (improved)
                match = re.search(r"```json\n(.*)\n```", json_response_str, re.DOTALL)  # Find JSON block
                if match:
                    json_response_str = match.group(1).strip() # Extract the JSON and remove whitespace
                    try:
                        json_response = json.loads(json_response_str)
                        sentiment = json_response["sentiment"]
                        confidence = float(json_response["confidence"])
                    except (json.JSONDecodeError, KeyError, ValueError) as e:
                        print(f"JSON Parse Error: {e}")
                        print("JSON String that caused the error:", json_response_str)
                        raise HTTPException(status_code=500, detail=f"Invalid Llama JSON format: {e}") # More specific error message
                else:
                    print("No JSON block found in Llama response:", json_response_str)
                    raise HTTPException(status_code=500, detail="No JSON found in Llama response") # More specific error message


            except Exception as e:
                print(f"Error during Llama analysis: {e}")
                raise HTTPException(status_code=500, detail="Error analyzing text with Llama.")

        else:
            raise HTTPException(status_code=400, detail="Invalid model choice.")

        return {"sentiment": sentiment, "confidence": confidence}

    except Exception as e:
        logger.exception("Error in analyze_text:")  # Log the exception with traceback
        raise HTTPException(status_code=422, detail=f"Invalid input: {e}") # Or 500 if it's a server error

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) # 0.0.0.0 makes it accessible from outside the container

