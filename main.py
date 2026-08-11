from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os


load_dotenv()


# =========================================================
# LLM
# =========================================================

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


# =========================================================
# TAVILY SEARCH TOOL
# =========================================================

tavily_search = TavilySearch(
    max_results=3,
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)


# =========================================================
# CALCULATOR TOOL
# =========================================================

@tool
def calculator(expression: str) -> str:
    """
    Calculate a mathematical expression.
    """

    try:

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception:

        return "Invalid mathematical expression."


# =========================================================
# CREATE AGENT
# =========================================================

search_agent = create_agent(

    model=llm,

    tools=[
        tavily_search,
        calculator
    ],

    system_prompt="""
You are SearchPilot AI, a helpful AI agent.

You have two tools:

1. Tavily Search
   - Use it for current information.
   - Use it for latest news.
   - Use it for recent events.
   - Use it for weather.
   - Use it for web searches.

2. Calculator
   - Use it for all mathematical calculations.
   - Never calculate mathematical expressions yourself.

Rules:

- If the user asks for current or recent information,
  use Tavily.

- If the user asks about weather,
  use Tavily.

- If the user asks for a calculation,
  use Calculator.

- If the user asks for both calculation and web information,
  use both tools.

- After using the required tools,
  provide one clear final answer.
"""
)


# =========================================================
# ASK AGENT
# =========================================================

res_agent = search_agent.invoke({

    "messages": [

        HumanMessage(
            content="What is the current weather in Delhi?"
        )

    ]

})


# =========================================================
# PRINT ANSWER
# =========================================================

print(
    res_agent["messages"][-1].content
)