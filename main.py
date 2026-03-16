from recipe_agent import CookingRecipeAgent
from utils.stream_utils import handle_stream, log_input, log_output


def main():

    print("\nCooking Recipe Agent (conversation mode)")
    print("Type 'exit' to stop.\n")

    agent = CookingRecipeAgent()

    while True:

        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        log_input(user_input, agent_name="CookingAgent")

        stream = agent.stream_recipe(user_input)

        response = handle_stream(stream, agent_name="CookingAgent")

        log_output(response, agent_name="CookingAgent")


if __name__ == "__main__":
    main()
    