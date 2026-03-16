# Cooking Recipe Agent

This project implements a simple AI agent that suggests cooking recipes based on ingredients provided by the user.

The agent uses a Large Language Model hosted on a remote Ollama server and streams the generated output to the terminal with structured logging.

The goal of the project is to demonstrate how an AI agent can solve a real-world problem: helping users decide what to cook using ingredients they already have at home.

---

# Project Overview

Users often have ingredients available but do not know what recipe they can prepare with them.

This agent addresses that problem by:

1. Asking the user which ingredients they have
2. Asking for dietary preferences
3. Sending the information to a language model
4. Generating a recipe suggestion
5. Streaming the result to the terminal

The system supports structured prompts and configurable model parameters such as temperature and top-p.

---

# Technologies Used

Python  
LangChain  
Ollama  
uv (Python environment manager)  
Remote LLM server (Nackademin infrastructure)

---

# Project Structure

```
cooking_recipe/
│
├── main.py
├── recipe_agent.py
├── .env
├── utils/
│   └── stream_utils.py
│
├── pyproject.toml
├── uv.lock
└── README.md
```

## File Description

main.py  
Entry point of the application. Handles user input and agent execution.

recipe_agent.py  
Defines the CookingRecipeAgent and configures the language model.

utils/stream_utils.py  
Utility file provided by the course to display streaming output and logging.

.env  
Stores configuration for the remote Ollama server and authentication token.

pyproject.toml  
Project dependencies managed by uv.

uv.lock  
Dependency lock file.

---

# Installation

## 1 Clone the Repository

```
git clone <repository-url>
cd cooking_recipe
```

---

## 2 Install uv

If uv is not installed:

Windows (PowerShell)

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS / Linux

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify installation:

```
uv --version
```

---

## 3 Install Dependencies

Create the environment and install dependencies:

```
uv sync
```

---

# Environment Configuration

Create a `.env` file in the root directory.

Example:

```
OLLAMA_BASE_URL=http://nackademin.icedc.se
OLLAMA_BEARER_TOKEN=your-token-here

```

## Variables

OLLAMA_BASE_URL  
URL of the remote Ollama server.

OLLAMA_BEARER_TOKEN  
Authentication token required by the server.

OLLAMA_MODEL  
Model used by the agent.  
Example: llama3.1:8b

---

# Running the Application

Run the agent with:

```
uv run python main.py
```

You will see:

```
Cooking Recipe Agent

Enter the ingredients you have:
```

Example input:

```
pasta, tomato, olive oil
```

Diet preference:

```
none
```

The agent will then stream the generated recipe.

---

# Agent Behavior

The agent is guided by a structured prompt.

The prompt includes:

Role  
The agent acts as an AI cooking assistant.

Task  
Generate a recipe using available ingredients.

Constraints  

Prefer recipes that use provided ingredients.  
Respect dietary preferences if provided.  
Keep recipes simple and practical.  

Output Format

Recipe Name  
Ingredients  
Steps 

The agent includes a tool for ingredient substitution.

When the user indicates that an ingredient is missing, 
the agent calls the substitution tool and incorporates 
the result into the prompt before generating the final recipe.

---

# Model Parameters

The model is configured with sampling parameters.

Temperature: 0.4  
Controls randomness and creativity.

Top-p: 0.9  
Controls nucleus sampling for token selection.

These parameters were tested to observe differences in recipe generation.

---
## Conversational Memory

The agent maintains a conversation history to support multi-turn interactions.

Each new user message is combined with previous messages and sent to the language model.  
This allows the agent to remember context and continue the conversation coherently.

Example:

User: I have pasta and tomato  
Agent: Suggests a recipe  

User: Can you make it vegan?  
Agent: Modifies the previous recipe accordingly.

# Author

Alessandro Abbate
