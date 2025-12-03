from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


load_dotenv()
model = ChatOpenAI()
chat_template=ChatPromptTemplate([
    ('system','You are a helpful customer support agent'),
    MessagesPlaceholder(variable_name='chat_history'),# creates a placeholder for set of messages
    ('human','{query}')
    ])

chat_history=[] ## reads the chathistory and appends to the list
with open('ChatModels/chat_history.txt') as f:
    chat_history.extend(f.readlines())

while True:
    user_input = input('You: ')
    prompt=chat_template.invoke({'chat_history':chat_history, #previous customer convo
                             'query':user_input}) 
    chat_history.append(HumanMessage(content=user_input))
    if user_input == 'exit':
        break
    result = model.invoke(prompt)
    chat_history.append(AIMessage(content=result.content))
    print("AI: ",result.content)

print(prompt)
