import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()


class CookingRecipeAgent:

    def __init__(self):

        base_url = os.getenv("OLLAMA_BASE_URL")
        bearer_token = os.getenv("OLLAMA_BEARER_TOKEN")
        model_name = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

        client_kwargs = {}

        if bearer_token:
            client_kwargs["headers"] = {
                "Authorization": f"Bearer {bearer_token}"
            }

        self.model = ChatOllama(
            model=model_name,
            base_url=base_url,
            client_kwargs=client_kwargs if client_kwargs else None,
            temperature=0.4,
            top_p=0.9
        )

        self.system_prompt = SystemMessage(
            content="""
You are an AI cooking assistant.

Your goal is to help users create simple recipes using the ingredients they already have.

Rules:
- Prefer recipes using the provided ingredients
- Respect dietary preferences
- Keep recipes simple
- Avoid unnecessary ingredients

Output format:

Recipe Name:
Ingredients:
Steps:
"""
        )

        # Memory for conversation
        self.history = []

    def stream_recipe(self, user_input: str):

        messages = [self.system_prompt] + self.history + [
            HumanMessage(content=user_input)
        ]

        raw_stream = self.model.stream(messages)

        for chunk in raw_stream:
            yield ("messages", (chunk, {"langgraph_node": "model"}))

        # Save user message in memory
        self.history.append(HumanMessage(content=user_input))