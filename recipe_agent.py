from langchain_ollama import ChatOllama


class CookingRecipeAgent:

    def __init__(self):

        self.model = ChatOllama(
            model="llama3"
            
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

        # stream from the model
        raw_stream = self.model.stream(self.system_prompt + prompt)

        # convert to LangGraph-like stream format
        for chunk in raw_stream:
            yield ("messages", (chunk, {"langgraph_node": "model"}))
