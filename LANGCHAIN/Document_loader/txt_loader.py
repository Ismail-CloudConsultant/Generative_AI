from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
model=ChatOpenAI()

loader=TextLoader('Document_loader/fox_Crow_story.txt',encoding='utf-8')
docs=loader.load()


# contains : 
    #1.Page contents
    #2.metadata={'source': 'Document_loader/fox_Crow_story.txt'}

Prompt=PromptTemplate(template='tell a short real life historical event based on this story - {story}',
               input_variables=['story'])

parser=StrOutputParser()

chain =Prompt | model | parser

print(chain.invoke({"story":docs[0].page_content}))