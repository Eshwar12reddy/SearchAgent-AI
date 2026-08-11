import ast
import operator
import os
from datetime import date

import streamlit as st

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SearchPilot AI",
    page_icon="🔎",
    layout="centered"
)


# =========================================================
# COLORFUL AI UI
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 15% 15%,
            rgba(20,184,166,0.30),
            transparent 30%
        ),
        radial-gradient(
            circle at 85% 20%,
            rgba(6,182,212,0.25),
            transparent 30%
        ),
        radial-gradient(
            circle at 50% 90%,
            rgba(59,130,246,0.25),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #020617,
            #0f172a,
            #083344
        );

    min-height: 100vh;
}


.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
    max-width: 850px;
}


h1 {
    color: #ecfeff !important;
    text-align: center;
    font-size: 46px !important;
    font-weight: 800 !important;

    text-shadow:
        0 0 10px rgba(34,211,238,0.8),
        0 0 25px rgba(20,184,166,0.5);
}


.subtitle {
    text-align: center;
    color: #a5f3fc;
    font-size: 18px;
    margin-top: -10px;
    margin-bottom: 35px;
}


.stTextInput label {
    color: #ccfbf1 !important;
    font-weight: 600 !important;
    font-size: 16px !important;
}


.stTextInput > div > div > input {
    background: rgba(240,253,250,0.96) !important;
    color: #0f172a !important;

    border: 2px solid #14b8a6 !important;
    border-radius: 14px !important;

    padding: 14px !important;
    font-size: 16px !important;

    box-shadow:
        0 0 15px rgba(20,184,166,0.20);
}


.stTextInput > div > div > input:focus {
    border: 2px solid #06b6d4 !important;

    box-shadow:
        0 0 10px rgba(6,182,212,0.5),
        0 0 25px rgba(20,184,166,0.3);
}


.stButton > button {
    width: 100%;

    border: none !important;
    border-radius: 14px !important;

    padding: 13px !important;
    margin-top: 12px;

    background: linear-gradient(
        90deg,
        #0d9488,
        #0891b2,
        #0284c7
    ) !important;

    color: white !important;

    font-size: 18px !important;
    font-weight: 700 !important;

    box-shadow:
        0 5px 20px rgba(6,182,212,0.30);

    transition: all 0.3s ease;
}


.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 8px 30px rgba(34,211,238,0.45);
}


.answer-title {
    color: #a5f3fc;

    font-size: 22px;
    font-weight: 700;

    margin-top: 30px;
    margin-bottom: 12px;
}


.answer-box {
    background: rgba(15,118,110,0.15);

    border:
        1px solid
        rgba(45,212,191,0.30);

    border-radius: 18px;

    padding: 25px;

    color: #ecfeff;

    font-size: 16px;
    line-height: 1.7;

    box-shadow:
        0 8px 35px rgba(0,0,0,0.25);

    backdrop-filter: blur(15px);
}


.footer {
    text-align: center;

    color: #67e8f9;

    font-size: 13px;

    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.title("🔎 SearchPilot AI")

st.markdown(
    """
    <div class="subtitle">
        An intelligent AI agent that searches the web,
        calculates, and uses tools to answer your questions.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# API KEYS
# =========================================================

groq_api_key = os.getenv("GROQ_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")


if not groq_api_key:
    st.error("GROQ_API_KEY is missing in your .env file.")
    st.stop()


if not tavily_api_key:
    st.error("TAVILY_API_KEY is missing in your .env file.")
    st.stop()


# =========================================================
# LLM
# =========================================================
# NOTE: llama-3.1-8b-instant was deprecated by Groq (announced
# June 17, 2026) and is being shut down on August 16, 2026.
# Using it now will either already fail or fail within days.
# Groq's recommended replacement is openai/gpt-oss-20b.

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    groq_api_key=groq_api_key,
    temperature=0
)


# =========================================================
# TAVILY SEARCH TOOL
# =========================================================
# TavilySearch reads TAVILY_API_KEY from the environment
# automatically (load_dotenv already put it there), so the
# explicit kwarg below is optional but kept for clarity.

tavily_search = TavilySearch(
    max_results=3,
    tavily_api_key=tavily_api_key
)


# =========================================================
# CALCULATOR TOOL
# =========================================================
# A bare eval() with an empty __builtins__ dict is NOT a safe
# sandbox — it can still be escaped (e.g. via __class__ /
# __subclasses__ tricks) to reach arbitrary Python objects.
# This version instead parses the expression into an AST and
# only allows numeric literals and basic arithmetic operators,
# which is much harder to break out of.

_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed.")
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](
            _safe_eval(node.left), _safe_eval(node.right)
        )
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("Unsupported expression.")


@tool
def calculator(expression: str) -> str:
    """
    Calculate a mathematical expression.

    Example:
    125 * 48
    """

    try:
        tree = ast.parse(expression, mode="eval")
        result = _safe_eval(tree.body)
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

    system_prompt=f"""
You are SearchPilot AI.

Today's real date is {date.today():%B %d, %Y}. Trust this over any
date you see inside search results — a search result's date is when
that page was published or updated, not "today". Never state a
different date as "today" or "as of today".

You have two tools:

1. Tavily Search
   - Use for current information.
   - Use for latest news.
   - Use for recent events.
   - Use for weather.
   - Use for web searches.

2. Calculator
   - Use for all mathematical calculations.
   - Never calculate mathematics yourself.

Rules:

- Current or recent information → Tavily.
- Weather → Tavily.
- Mathematical calculation → Calculator.
- Both calculation and web information → use both tools.
- After using the tools, provide one clear final answer.
"""
)


# =========================================================
# HELPER: normalize the final message content to a string
# =========================================================
# Tool-calling models sometimes return `content` as a list of
# content blocks (e.g. [{"type": "text", "text": "..."}])
# instead of a plain string. This flattens either shape safely.

def extract_answer_text(message_content) -> str:
    if isinstance(message_content, str):
        return message_content

    if isinstance(message_content, list):
        parts = []
        for block in message_content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and "text" in block:
                parts.append(block["text"])
        return "\n".join(parts) if parts else str(message_content)

    return str(message_content)


# =========================================================
# USER INPUT
# =========================================================

question = st.text_input(
    "Ask your question:",
    placeholder="Example: Calculate 125 * 48 and tell me the latest AI news."
)


# =========================================================
# RUN AGENT
# =========================================================

if st.button("🚀 Ask Agent"):

    if not question:

        st.warning(
            "Please enter a question."
        )

    else:

        try:

            with st.spinner(
                "🤖 Agent is thinking..."
            ):

                response = search_agent.invoke(
                    {
                        "messages": [
                            HumanMessage(
                                content=question
                            )
                        ]
                    }
                )

                answer = extract_answer_text(
                    response["messages"][-1].content
                )


            # =================================================
            # DISPLAY ANSWER
            # =================================================

            st.markdown(
                """
                <div class="answer-title">
                    🤖 SearchPilot AI
                </div>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                f"""
                <div class="answer-box">
                    {answer}
                </div>
                """,
                unsafe_allow_html=True
            )


        except Exception as e:

            error_message = str(e)

            if (
                "RateLimitError" in error_message
                or "429" in error_message
            ):

                st.warning(
                    "⏳ Groq rate limit reached. "
                    "Please wait a few seconds and try again."
                )

            else:

                st.error(
                    f"Something went wrong: {error_message}"
                )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Powered by Eshwar Reddy
    </div>
    """,
    unsafe_allow_html=True
)