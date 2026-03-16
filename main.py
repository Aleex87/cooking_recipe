from recipe_agent import CookingRecipeAgent


def main():

    print("\n🍳 Cooking Recipe Agent\n")

    agent = CookingRecipeAgent()

    ingredients = input("Enter the ingredients you have: ")
    diet = input("Dietary preference (vegan, gluten-free, vegetarian, none): ")


    recipe = agent.get_recipe(ingredients, diet)

    print("\nSuggested recipe:\n")
    print(recipe)


if __name__ == "__main__":
    main()
    