# sentimentAnalyzer
This application estimates your sentences to negative or positive and give confidence level from 0.0 to 1.0. Repository consist of movieanalyzer backend and my-app fronted.

## MovieAPI (Backend)
### Dependencies
Needed dependencies are Transformers, Groq, Unicorn, Pydantic, and FastAPI.
```
pip install transformers groq uvicorn pydantic fastapi
```
## Instructions to run
Clone the repositorio.
```
git clone https://github.com/ranurm/sentimentAnalyzer.git
cd sentimentAnalyzer
cd movieanalyzer
```
Set GROQ_API_KEY environment variable.
```
export GROQ_API_KEY="your_groq_api_key"
```
You can run the FastAPI server with Uvicorn.
```
uvicorn movieAPI:app --reload
```
With PowerCell can be tested with command:
```
Invoke-WebRequest -Uri "http://127.0.0.1:8000/translate/" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"text": "Hello, world!", "target_language": "fi"}'
```
Also curl for other devices:
```
curl -X POST -H "Content-Type: application/json" -d '{"text": "Hello, world!", "target_language": "fi"}' http://127.0.0.1:8000/translate
```
