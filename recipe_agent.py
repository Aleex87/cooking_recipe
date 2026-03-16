from langchain_ollama import ChatOllama


class CookingRecipeAgent:
    """
    CookingRecipeAgent suggests recipes based on ingredients provided by the user.
    It uses a local LLM via Ollama.
    """

    def __init__(self):
        # Initialize the local LLM model
        self.model = ChatOllama(model="llama3")

        # System instructions for the agent
        self.system_prompt = """
        You are a helpful cooking assistant.

        Your task is to suggest recipes based on ingredients provided by the user.

        Always include:
        - Recipe name
        - Ingredient list
        - Step-by-step cooking instructions

        Respect dietary restrictions if provided.
        """

    def get_recipe(self, ingredients: str, diet: str) -> str:
        """
        Generate a recipe using the provided ingredients.
        """

        prompt = f"""
        The user has the following ingredients:

        {ingredients}

         Dietary preference:
        {diet}

        Suggest a recipe that respects the dietary preference if possible.
        """

        print("\n🤖 Generating recipe...\n")

        full_response = ""

        for chunk in self.model.stream(self.system_prompt + prompt):
            text = chunk.content
            print(text, end="", flush=True)
            full_response += text

        print("\n")

        return full_response