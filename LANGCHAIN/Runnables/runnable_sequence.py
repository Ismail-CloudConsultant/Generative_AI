# RunnableSequence is LangChain’s way of composing multiple steps into a declarative execution graph 
# where the output of one step becomes the input to the next.It constructs a declarative execution graph where each step is a standard Runnable with guaranteed 
# Nesting functions executes immediately and gives no structure.
# RunnableSequences define a graph that executes with controlled, observable, LLM-optimized behavior.

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence

load_dotenv()

Prompt= PromptTemplate(
    template="write a cunning joke on {topic}",
    input_variables=['topic']
)

model=ChatOpenAI()
parser=StrOutputParser()

Prompt2=PromptTemplate(
    template="understand the joke and give a serious comeback of this -  joke: {text}",
    input_variables=['text']
)

first_chain = RunnableSequence(Prompt, model, parser)
second_chain = RunnableSequence(Prompt2, model, parser)

# Get first response
first_output = first_chain.invoke({'topic': 'corporate sick leave'})
print("FIRST RESPONSE (Joke):\n", first_output)

# # Get second response
final_output = second_chain.invoke({'text': str(first_output)})
print("\n serious Comeback :\n", final_output)

# Why did the corporate sick leave policy change? Because they finally realized the employees were faking it to get an extra day off!

#  Serious comeback: It's important for companies to have trust in their employees and treat their well-being seriously. If employees are constantly feeling the need to fake being sick to get a day off, it may be worth examining other issues within the workplace that are causing this behavior. A strong and honest relationship between employers and employees is crucial for a healthy work environment. 