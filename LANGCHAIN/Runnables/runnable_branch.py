#TASK -model will ask me one question about one topic , if my answer is correct , 
# it will give good , if my answer is close then it will give just correction , 
# else if wrong it will give short explaination. 

# RunnableLambda = Do Something AND RunnableBranch = Choose Something
#  conditional logic
#  if–else
#  routing
#  task switching
#  decision making

# branch = RunnableBranch(
#     # IF condition
#     (
#         lambda x: <condition_1>, 
#         <runnable_if_true>
#     ),

#     # ELIF condition
#     (
#         lambda x: <condition_2>, 
#         <runnable_if_true_2>
#     ),

#     # ELSE (default)
#     <default_runnable>
# )

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence, RunnableLambda, RunnableBranch
from langchain_core.output_parsers import PydanticOutputParser,StrOutputParser
from pydantic import BaseModel
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from typing import Optional,Literal

load_dotenv()
ask_prompt = PromptTemplate(
    template="Ask the user ONE quiz question about {topic}. Only ask the question.",
    input_variables=["topic"]
)

# --- Structured output for review ---
class Review(BaseModel):
    sentiment: Literal["Correct", "Wrong"] = Field(
        description="If answer is absolutely correct: Correct. If answer is wrong or close: Wrong."
    )

model = ChatOpenAI(model="gpt-4o-mini")

# normal text parser
text_parser = StrOutputParser()

# structured LLM
structured_model = model.with_structured_output(Review)

# STEP 1 → Ask question
ask_chain = ask_prompt | model | text_parser

# Ask question
question = ask_chain.invoke({"topic": "machine learning"})
print("QUESTION:", question)

user_answer = input("Your Answer: ")


review_prompt = PromptTemplate(
    template="""
Question: {question}
User Answer: {answer}

Evaluate the user's answer 
""",
    input_variables=["question", "answer"]
)
review_chain = review_prompt | structured_model
review = review_chain.invoke({"question": question, "answer": user_answer})
print("Structured Review:", review)




# Runnable for CORRECT
correct_runnable = (
    PromptTemplate(
        template="The user's answer is correct. Give a short praise.",
        input_variables=[]
    )
    | model
    | text_parser
)

# Runnable for WRONG (close or wrong)
wrong_runnable = (
    PromptTemplate(
        template="""
The user's answer was wrong or partially correct.

Question: {question}
User Answer: {answer}

Give EITHER:
- a short correction if the answer is close  
- OR a short explanation if completely wrong  
"Keep the answer under 4 lines."
""",
        input_variables=["question", "answer"]
    )
    | model
    | text_parser
)

# --- RunnableBranch ---
branch = RunnableBranch(

    (
        lambda x: x["sentiment"] == "Correct",
        correct_runnable
    ),


    wrong_runnable
)



final_result = branch.invoke({
    "sentiment": review.sentiment,
    "question": question,
    "answer": user_answer
})

print("\nFINAL FEEDBACK:\n", final_result)