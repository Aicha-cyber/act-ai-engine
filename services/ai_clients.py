import os
import requests
import json
from openai import OpenAI
from dotenv import load_dotenv


# read.env and populate process env (API keys)
load_dotenv()


class AIClients:
    def __init__(self):
        # Initialize clients
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.groq_api_key = os.getenv('GROQ_API_KEY')

    # OpenAI GPT-4 for research analysis
    def openai_analysis(self, prompt, model="gpt-4"):
        try:
            # call chat completions API
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],  # single turn call
                temperature=0.7,  # moderate creativity
                max_tokens=1000  # cap output length
            )
            return response.choices[0].message.content  # extract generated text
        except Exception as e:
            return f"OpenAI Error: {str(e)}"  # error as a string

    # Groq API for fast financial analysis
    def groq_analysis(self, prompt, model="mixtral-8x7b-32768"):
        try:
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 1000
            }

            response = requests.post(   # HTTP POST to Groq's Chat Completions endpoint
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:  # if successful, parse and return content
                return response.json()['choices'][0]['message']['content']
            else:
                return f"Groq API Error: {response.text}"  # else return server error

        except Exception as e:
            return f"Groq Connection Error: {str(e)}"  # for timeout , network or other exceptions

    # Ollama Local - Llama 3 for content generation
    def ollama_llama_analysis(self, prompt):
        try:
            data = {
                "model": "llama3",
                "prompt": prompt,  # prompt text
                "stream": False  # non streaming response request
            }

            response = requests.post(  # POST to local Ollama REST API
                "http://localhost:11434/api/generate",
                json=data,
                timeout=30
            )

            if response.status_code == 200:  # If success, return the response field
                return response.json()['response']
            else:
                return f"Ollama Error: {response.text}"  # Return Ollama error text

        except Exception as e:
            return f"Ollama Connection Error: {str(e)}"  # return other exceptions

    # Ollama Local - Mistral for risk assessment
    def ollama_mistral_analysis(self, prompt):
        try:
            data = {
                "model": "mistral",  # Local Mistral model name in Ollama
                "prompt": prompt,
                "stream": False
            }

            response = requests.post(
                "http://localhost:11434/api/generate",  # Same local endpoint, different model
                json=data,
                timeout=30  # 30 seconds timeout give up
            )

            if response.status_code == 200:
                return response.json()['response']
            else:
                return f"Ollama Mistral Error: {response.text}"

        except Exception as e:
            return f"Ollama Mistral Connection Error: {str(e)}"

    # Fallback to simple analysis if LLMs fail
    def fallback_analysis(self, ticker, analysis_type):
        fallbacks = {
            "research": f"Basic research analysis for {ticker}. LLM integration required.",
            "accounting": f"Financial ratios for {ticker}. Enable AI for detailed analysis.",
            "recommendation": "HOLD - Enable AI for personalized recommendations",
            "blog": f"# {ticker} Analysis\n\nAI-powered analysis coming soon."
        }
        return fallbacks.get(analysis_type, "Analysis unavailable")


# Singleton instance
ai_clients = AIClients()
