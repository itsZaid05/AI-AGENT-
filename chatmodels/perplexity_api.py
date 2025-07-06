from langchain_perplexity import ChatPerplexity
from dotenv import load_dotenv

load_dotenv()

model = ChatPerplexity(
    model="llama-3.1-sonar-small-128k-online",  # or another Perplexity model
    temperature=0,
    max_tokens=100
)

result = model.invoke("Write a 5 line poem on bihar")
print(result.content)
