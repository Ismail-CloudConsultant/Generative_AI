from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field
from typing import Optional,Literal

from huggingface_hub import login
login("PASTE_cODE_HERE")

llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)


class Review(BaseModel):
    key_themes:list[str]= Field(description="Write down all the key themes discussed in the review in a list")
    summary: str= Field(description="A breif summary of the review")
    sentiment:Literal["Negative", "Postive" ,"Neutral","Mixed"]=Field(description="returns sentiment IN Negative, Postive ,Neutral")
    rating:int=Field(description="Maximum out of 10")
    pros: Optional[list[str]]= Field(description="Write down all the pros inside a list")
    cons: Optional[list[str]]= Field(description="Write down all the cons inside a list")

parser = PydanticOutputParser(pydantic_object=Review)

template = PromptTemplate(
    template='Generate a detailed review with mixed sentiments for {Phone} mobile \n {format_instruction}',
    input_variables=['Phone'],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)

chain = template | model | parser

final_result = chain.invoke({'Phone':'Nokia 3310'})

print(final_result)