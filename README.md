# 🔎 SearchPilot AI

## Intelligent Multi-Tool AI Agent

**Live Demo:** https://searchagent-ai.streamlit.app/

---

## 📌 Overview

**SearchPilot AI** is an intelligent **AI Agent** built using **LangChain, Groq, Tavily, and Streamlit**.

The system understands the user's question and **automatically selects the appropriate tool** to provide the required information.

It can perform **real-time web searches, mathematical calculations, and weather-related queries**. The agent can also use multiple tools when a question requires information from different sources.

---

## 🚀 Features

✅ AI-powered question answering
✅ Real-time web search using Tavily
✅ Mathematical calculations using Calculator Tool
✅ Weather query handling
✅ Automatic tool selection
✅ Multiple tools in a single query
✅ LangChain-based AI Agent
✅ Interactive Streamlit interface
✅ Secure API key management
✅ Real-time information retrieval

---

## 🧠 How It Works

```text
User Question
      |
      ↓
SearchPilot AI Agent
      |
      ↓
Understand User Query
      |
      ↓
Select Required Tool
      |
 ┌────┼─────────────┐
 ↓    ↓             ↓
Tavily Calculator  Weather
 ↓    ↓             ↓
Web   Math       Weather
Search Result     Data
 └────┼─────────────┘
      ↓
    Groq LLM
      ↓
Final Answer
```

---

## 🛠️ Tech Stack

### Programming Language

* Python

### AI / LLM

* Groq
* LLM
* LangChain

### AI Agent Framework

* LangChain Agents
* Tool Calling

### Tools

* Tavily Search
* Calculator Tool
* Weather Tool

### Application Framework

* Streamlit

### Environment & Security

* Python-dotenv
* Environment Variables

---

## 📂 Project Structure

```text
SearchPilot-AI/
│
├── app.py                    # Streamlit application
├── agent.py                  # AI Agent and tool configuration
├── tools.py                  # Search, calculator and weather tools
├── requirements.txt          # Project dependencies
├── .env                      # API keys (local only)
├── .gitignore                # Ignore sensitive files
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/SearchPilot-AI.git
```

### 2. Navigate into Project

```bash
cd SearchPilot-AI
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux/Mac**

```bash
source venv/bin/activate
```

---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Configure API Keys

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Never upload the `.env` file or API keys to GitHub.

---

## ▶️ Run Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🔄 Application Workflow

1. User enters a question.
2. SearchPilot AI analyzes the query.
3. The AI Agent determines which tool is required.
4. The selected tool performs the required operation.
5. Tool results are returned to the agent.
6. Groq LLM processes the results.
7. The final answer is displayed in Streamlit.

For example:

```text
"What is the current weather in Hyderabad?"
              ↓
        Weather Tool
              ↓
        Weather Result
              ↓
          Groq LLM
              ↓
        Final Response
```

For a mathematical question:

```text
"What is 125 × 48?"
        ↓
Calculator Tool
        ↓
     6000
        ↓
  Final Answer
```

For a current-information question:

```text
"What are the latest AI developments?"
              ↓
         Tavily Search
              ↓
       Web Search Results
              ↓
           Groq LLM
              ↓
        Final Answer
```

---

## 🤖 AI Agent Capabilities

| Tool             | Purpose                                 |
| ---------------- | --------------------------------------- |
| 🔎 Tavily Search | Real-time web information               |
| 🧮 Calculator    | Mathematical calculations               |
| 🌤️ Weather Tool | Weather-related queries                 |
| 🧠 Groq LLM      | Reasoning and final response generation |

---

## 📊 Project Details

**Project Type:** Intelligent Multi-Tool AI Agent

**Framework:** LangChain

**LLM:** Groq

**Web Search:** Tavily

**Interface:** Streamlit

**Core Capability:** Automatic Tool Selection

**Output:** AI-generated response based on tool results

---

---

## 🔮 Future Improvements

* Add more external tools
* Add database search
* Add PDF/document search
* Add RAG capabilities
* Add conversation memory
* Add voice interaction
* Add multi-agent architecture
* Add authentication
* Improve agent reasoning and tool selection
* Deploy with scalable cloud infrastructure

---

## 👨‍💻 Author

**P.Manikanteswara Reddy**

AI & Data Science Enthusiast

---

## ⭐ If you like this project

Give this repository a ⭐ and feel free to explore!
