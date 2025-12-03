from langchain_openai import ChatOpenAI 
from dotenv import load_dotenv

load_dotenv()

model= ChatOpenAI(model='gpt-4',temperature=1.5)
result=model.invoke("capital of wonderland - haha?")
print(result.content)