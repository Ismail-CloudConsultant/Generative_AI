#TASK1- ask model 1 to create a report on one topic and  ask model 2 to create quiz on same topic

#TASK2- ask model 1 to review model 2 output   and  ask model 2 to review model 1 output 

# ask model 3 to be the judge

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.runnables import RunnableParallel


from huggingface_hub import login
login() ## paste your API key here

llm1 = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    task="text-generation"
)

llm2 = HuggingFaceEndpoint(
    repo_id="distilbert/distilgpt2",
    task="text-generation"
)
model1=ChatHuggingFace(llm=llm1)
model2=ChatHuggingFace(llm=llm2)

load_dotenv()
model3=ChatOpenAI()


prompt1 = PromptTemplate(
    template="Generate 10 lines of important notes on: {Topic}",
    input_variables=["Topic"]
)

prompt2 = PromptTemplate(
    template="Generate 10 quiz questions on: {Topic}",
    input_variables=["Topic"]
)

review_quiz_prompt = PromptTemplate(
    template=(
        "You are model 1 reviewing a quiz.\n"
        "Topic: {Topic}\n\n"
        "Quiz:\n{quiz}\n\n"
        "Provide a detailed review."
    ),
    input_variables=["quiz", "Topic"]
)

review_notes_prompt = PromptTemplate(
    template=(
        "You are model 2 reviewing notes.\n"
        "Topic: {Topic}\n\n"
        "Notes:\n{notes}\n\n"
        "Provide a detailed review."
    ),
    input_variables=["notes", "Topic"]
)

parser = StrOutputParser()

# ---------------------------
# TASK 1 – Generate Notes + Quiz
# ---------------------------

parallel_chain_TASK1 = RunnableParallel({
    "notes": prompt1 | model1 | parser,
    "quiz": prompt2 | model2 | parser,
})

# ---------------------------
# TASK 2 – Cross Review
# ---------------------------

parallel_chain_TASK2 = RunnableParallel({
    "review_quiz_by_model1": review_quiz_prompt | model1 | parser,
    "review_notes_by_model2": review_notes_prompt | model2 | parser,
})

# ---------------------------
# JUDGE
# ---------------------------

judge_prompt = PromptTemplate(
    template=(
        "Model 1 wrote NOTES, Model 2 wrote QUIZ.\n"
        "Both models reviewed each other.\n\n"
        "=== REVIEW OF QUIZ BY MODEL 1 ===\n{review_quiz}\n\n"
        "=== REVIEW OF NOTES BY MODEL 2 ===\n{review_notes}\n\n"
        "You are the judge (model 3). Decide:\n"
        "1. Which model performed better and why?\n"
        "2. Rate each model from 1–10.\n"
        "3. Give a final recommendation.\n"
    ),
    input_variables=["review_notes", "review_quiz"]
)

judge_chain = judge_prompt | model3 | parser

# ---------------------------
# RUN THE PIPELINE
# ---------------------------

topic = "unsecured lending"

task1_output = parallel_chain_TASK1.invoke({"Topic": topic})

task2_output = parallel_chain_TASK2.invoke({
    "notes": task1_output["notes"],
    "quiz": task1_output["quiz"],
    "Topic": topic
})

judge_output = judge_chain.invoke({
    "review_notes": task2_output["review_notes_by_model2"],
    "review_quiz": task2_output["review_quiz_by_model1"],
})

print("\n===== JUDGE VERDICT =====\n")
judge_chain.get_graph().print_ascii()