from recipe_agent import CookingRecipeAgent
from utils.stream_utils import handle_stream, log_input, log_output


def main():
    print("\nCooking Recipe Agent\n")

    agent = CookingRecipeAgent()

    ingredients = input("Enter the ingredients you have: ")
    diet = input("Dietary preference (vegan, vegetarian, gluten-free, none): ")

    user_input = f"Ingredients: {ingredients} | Diet: {diet}"

    log_input(user_input, agent_name="CookingAgent")

    stream = agent.stream_recipe(ingredients, diet)

    final_response = handle_stream(stream, agent_name="CookingAgent")

    log_output(final_response, agent_name="CookingAgent")


if __name__ == "__main__":
    main()
    
