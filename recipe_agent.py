import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()


class CookingRecipeAgent:
    def __init__(self):
        base_url = os.getenv("OLLAMA_BASE_URL")
        bearer_token = os.getenv("OLLAMA_BEARER_TOKEN")

        # Configure headers only if a token exists
        client_kwargs = {}
        if bearer_token:
            client_kwargs["headers"] = {
                "Authorization": f"Bearer {bearer_token}"
            }

        self.model = ChatOllama(
        model="llama3.1:8b",
        base_url=base_url,
        client_kwargs=client_kwargs if client_kwargs else None,
        temperature=0.9,
        top_p=0.1
    )

        self.system_prompt = """
You are an AI cooking assistant.

Your goal is to help users create simple recipes using the ingredients they already have.

TASK
Generate a recipe suggestion based on the user's ingredients.

CONSTRAINTS
- Prefer recipes that use the provided ingredients
- Respect dietary preferences if provided
- Keep recipes simple and practical
- Avoid unnecessary ingredients

OUTPUT FORMAT
Recipe Name:
Ingredients:
Steps:
"""

    def stream_recipe(self, ingredients: str, diet: str):
        prompt = f"""
Ingredients:
{ingredients}

Dietary preference:
{diet}

Suggest a recipe using these ingredients and respecting the diet.
"""

        raw_stream = self.model.stream(self.system_prompt + prompt)

        # Convert to the format expected by stream_utils
        for chunk in raw_stream:
            yield ("messages", (chunk, {"langgraph_node": "model"}))
            