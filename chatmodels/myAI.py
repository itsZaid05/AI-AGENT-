from langchain_perplexity import ChatPerplexity
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from dotenv import load_dotenv

load_dotenv()

model=ChatPerplexity(
    model="llama-3.1-sonar-small-128k-online",
    temperature =0)

chat_history=[
    SystemMessage(content="YOU ARE A HELPFULL AI ASSISTANCE")

]

while True:
    user_input= input("YOU: ")
    chat_history.append(HumanMessage(content=user_input))
    if user_input=="exit":
        break
    result=model.invoke(chat_history)
    chat_history.append(AIMessage(content=result.content))
    print("AI: ",result.content)
print (chat_history)
