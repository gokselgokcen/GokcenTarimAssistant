Gökcen Tarım AI Agent 

A smart sidebar assistant designed for an agricultural supply company. This project implements an Adaptive RAG architecture using LangGraph to handle customer inquiries, check real-time stock prices, and generate sales leads.

🎯 Key Features

Intelligent Routing: The agent dynamically decides whether to use RAG (for company info), External Tools (for prices/weather), or Direct Chat based on user intent.

Real-Time Data (Airtable): Fetches up-to-date product prices and stock status directly from an Airtable database.

Lead Generation: Captures user contact details during conversation and saves them to a CRM (Airtable).

Self-Corrective RAG: Verifies retrieved documents against the user's question to reduce hallucinations.

Web Search: Uses Tavily API to answer general agricultural questions not found in the internal knowledge base.

🛠️ Tech Stack

Orchestration: LangGraph (Stateful, cyclic workflow).

LLM: Google Gemini.

Framework: LangChain.

Vector Store: ChromaDB.

Tools & Database: Airtable API, Tavily Search API.

🏗️ Workflow Overview

Router: Classifies the input (e.g., Price Query vs. Company Policy).

RAG Branch: Retrieves documents -> Grades relevance -> Generates answer (or re-writes query if irrelevant).

Tool Branch: Executes API calls (Read Prices / Write Leads) -> Generates natural language response.

Direct Branch: Handles casual conversation (chit-chat) instantly.

🚀 Setup
Bash
# Clone the repo
git clone https://github.com/yourusername/gokcen-tarim-ai.git

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (.env)
GOOGLE_API_KEY=...
AIRTABLE_API_KEY=...
TAVILY_API_KEY=...

# Run the agent
python main.py