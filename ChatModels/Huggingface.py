from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
    #api_key=os.getenv("HF_TOKEN"),
    max_new_tokens=128,
    temperature=0.3
)

response = llm.invoke("What is the capital of India?")
print(response)