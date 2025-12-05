from langchain_community.document_loaders import TextLoader,DirectoryLoader,PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

loader=DirectoryLoader(
    path='Document_loader',
    glob='*.pdf',
    loader_cls=PyPDFLoader
)

docs=loader.load()

print((docs[0].page_content))