from langchain_groq import ChatGroq
import os
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage
from dotenv import load_dotenv

load_dotenv()

def loadModel():
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    model  = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    )

    return model


