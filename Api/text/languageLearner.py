import os
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain.prompts import PromptTemplate
from config.model import loadModel

# ========================== #
#    Global Memory (Persistent)
# ========================== #

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ========================== #
#    Load Learning Context
# ========================== #

with open("prpmpts/language_learner.md", "r", encoding="utf-8") as file:
    learning_context = file.read()

# Add system message only once
if not memory.chat_memory.messages:
    system_message = SystemMessage(content=learning_context)
    memory.chat_memory.add_message(system_message)


def learningAgent(query: str):
    """Initializes and returns the English Learning Assistant agent, keeping memory persistent."""

    # Define Tool for Learning Assistance
    def learning_context_tool(query: str) -> str:
        """Returns the structured learning roadmap for new users or follows MCQ practice."""
        if "roadmap" in query.lower() or "first-time user" in query.lower():
            return f"### 🛤 **Personalized Roadmap**\n\n{learning_context}\n\n🔹 *Follow the roadmap format strictly.*"
        return f"{learning_context}\n\nUser Query: {query}"

    tools = [
        Tool(
            name="English Learning Assistant",
            func=learning_context_tool,
            description="Provides an English learning roadmap, interactive exercises, and fluency enhancement tips."
        )
    ]

    # Initialize Learning Agent (Memory remains the same)
    agent = initialize_agent(
        tools=tools,
        llm=loadModel(),
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
        handle_parsing_errors=True
    )

    response = agent.run(query)
    return response

# ========================== #
#    Run Example
# ========================== #

if __name__ == "__main__":
    query = "I want to learn English."
    response = learningAgent(query)
    print(response)
