from langchain.tools import tool


@tool
def ingredient_substitution(ingredient: str) -> str:
    """
    Suggest a possible substitution for a missing ingredient.
    """
    return f"Suggested substitution for {ingredient}: use a similar ingredient suitable for the recipe."