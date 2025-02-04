# sentimentAnalyzer
This application estimates your sentences to negative or positive and give confidence level from 0.0 to 1.0. Repository consist of movieanalyzer backend and my-app fronted.

## MovieAPI (Backend)
### Dependencies
Needed dependencies are Transformers, Groq, Unicorn, Pydantic, and FastAPI.
```
pip install transformers groq uvicorn pydantic fastapi
```
### Instructions to run
Clone the repository.
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
### Calling API locally without frontend
Curl example:
```
curl -X POST "http://127.0.0.1:8000/analyze/"      -H "Content-Type: application/json"      -d '{"text": "Bad!!", "model": "llama"}'
```
Postman example:
![image](https://github.com/user-attachments/assets/591008bc-c9db-4297-b01d-d359f88c6acf)

## my-app (Frontend)
### Instructions to run
Clone the repository.
```
git clone https://github.com/ranurm/sentimentAnalyzer.git
cd sentimentAnalyze
cd my-app
```
Run the app.
```
npm install
npm run
```
