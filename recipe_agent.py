import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from tools import ingredient_substitution

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

        self.tools = [ingredient_substitution]

        self.system_prompt = SystemMessage(
            content="""
You are a professional AI cooking assistant.

ROLE
You help users create simple and practical recipes based on the ingredients they already have.

GOAL
Generate a recipe suggestion that maximizes the use of the user's available ingredients while respecting any dietary preferences.

INPUT
The user may provide:
- A list of ingredients
- Dietary preferences
- Follow-up questions
- Information about missing ingredients

CONSTRAINTS
- Prefer recipes that use the provided ingredients
- Respect dietary preferences if specified
- Keep recipes simple and practical
- Avoid introducing too many extra ingredients
- If an ingredient is missing, use the substitution tool result if available
- Use previous conversation context when relevant

OUTPUT FORMAT

Recipe Name:

Ingredients:
- ingredient 1
- ingredient 2

Steps:
1. Step one
2. Step two

Optional Tip:
A short cooking tip or variation
"""
        )

        self.history = []

    def _maybe_use_tool(self, user_input: str):

        text = user_input.lower()

        # detect if the user is missing olive oil
        if "olive oil" in text and ("no" in text or "missing" in text or "without" in text):

            ingredient = "olive oil"

            print(f"\n[TOOL CALL] ingredient_substitution → {ingredient}")

            result = ingredient_substitution.invoke(ingredient)

            print(f"[TOOL RESULT] {result}\n")

            return result

        return ""

    def stream_recipe(self, user_input: str):

        tool_result = self._maybe_use_tool(user_input)

        enriched_input = user_input
        if tool_result:
            enriched_input += f"\n\nTool result:\n{tool_result}"

        messages = [self.system_prompt] + self.history + [
            HumanMessage(content=enriched_input)
        ]

        raw_stream = self.model.stream(messages)

        full_response = ""

        for chunk in raw_stream:
            if getattr(chunk, "content", None):
                text = chunk.content
                if isinstance(text, str):
                    full_response += text

            yield ("messages", (chunk, {"langgraph_node": "model"}))

        self.history.append(HumanMessage(content=user_input))
        if full_response.strip():
            self.history.append(AIMessage(content=full_response))