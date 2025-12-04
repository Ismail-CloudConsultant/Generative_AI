from langchain_core.runnables import RunnableSequence, RunnableParallel,RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
model=ChatOpenAI()
from langchain_core.prompts import PromptTemplate


def get_review(_):
    return input("Enter your review: ")

def validate_review(review):
    words = review.split()
    n = len(words)

    if n < 3:
        print("Too short! Please provide a longer review.")
        return input("Enter review again: ")

    if n > 20:
        print("Too long! Please provide a shorter review.")
        return input("Enter review again: ")

    return review

def prepare_feedback(inputs):
    review = inputs["validated"]
    count = len(review.split())
    return f"({count} words): {review}"

parser=StrOutputParser()

Prompt=PromptTemplate(
    template= 'User has written a review {text}, give a short response on this',
    input_variables=['text'])

pipeline = RunnableSequence(

        # Step 1: Ask user for review
        RunnableLambda(get_review),

        # Step 2: Keep original + validate in parallel
        RunnableParallel({
            "original": RunnablePassthrough(),       # keep original review
            "validated": RunnableLambda(validate_review)
        }),
        # Step 3:  feedback formatting
        RunnableLambda(prepare_feedback),
        parser,

         # Step 4: model feeding
        model,parser

)

# Run
output = pipeline.invoke(None)
print("\nFinal Output:")
print(output)
