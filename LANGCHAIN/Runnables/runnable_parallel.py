from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnableSequence
from dotenv import load_dotenv

load_dotenv()
model=ChatOpenAI()

prompt1=PromptTemplate(template='create a post for linkdln on topic - {topic}',
                       input_variables=['topic']

)

prompt2=PromptTemplate(template='i am a posting on linkdln about topic - {topic}, give me some hastags',
                       input_variables=['topic']

)
parser=StrOutputParser()

parallel_chains=RunnableParallel({
    'post':RunnableSequence(prompt1,model,parser),
    'hastags':RunnableSequence(prompt2,model,parser)
})

result=parallel_chains.invoke({'topic':'posture in interview'})
print(result)