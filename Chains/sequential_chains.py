from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from huggingface_hub import login
login() ## paste your API key here

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    task="text-generation"
)


prompt1=PromptTemplate(
    template="Generate a SERIOUS detailed report on {topic}",
    input_variables=['topic']
)

prompt2= PromptTemplate(
    template='Generate 2 lines of most short funny SARCASTIC COMMENTARY from the following text \n {text}',
    input_variables=['text']
)

model=ChatHuggingFace(llm=llm)

parser=StrOutputParser()

chain=prompt1 | model | parser | prompt2 | model | parser

result = chain.invoke({'topic':'SPEED in karate'})

print(result)

# "So, basically, if you just keep punching trees until you turn into a ninja, you'll achieve karate mastery? We're encouraged!"
# "Hard work? Sounds like the kind of thing that'll leave you bruised, tired, and questioning your entire life choices. Now, where's my oxygen-thieving, sleep-depriving, power-nap-induced meditation app?"
