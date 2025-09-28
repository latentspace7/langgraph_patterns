from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

# Initialize the chat model
chat_llm = init_chat_model("anthropic:claude-3-7-sonnet-latest", temperature=0)

# Define the prompt template
executor_prompt = ChatPromptTemplate.from_messages([
    ("placeholder", "{messages}")
])

# Create the executor chain
executor = executor_prompt | chat_llm
