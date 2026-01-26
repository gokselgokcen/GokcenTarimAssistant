import langchainhub as hub
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
template = template = """You are the official AI assistant of 'Gökcen Tarım', a professional agricultural supply store.

    Use the provided information to answer the user's question. 
    You have two sources of information:
    1. Technical Documents (Context): {context}
    2. Real-time Price/Stock Data (Airtable): {tool_output}

    Rules:
    1. If there is price or stock information in 'tool_output', prioritize it and state it clearly (e.g., 'Gökcen Tarım'da Üre fiyatı 1.300 TL'dir').
    2. If the answer is not in either source, clearly state that you don't have this specific information but can help with other farming topics.
    3. Your tone should be helpful, professional, and grounded in agricultural expertise.
    4. Keep your response concise (maximum 3-4 sentences).
    5. Always answer in the language the user is speaking.
    
    Question:
    {question}
    
    Answer:
    """

gen_prompt = ChatPromptTemplate.from_template(template)

# --- FINAL GENERATION CHAIN ---
generation_chain = gen_prompt | llm | StrOutputParser()