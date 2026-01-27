from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Optional
load_dotenv()

class CustomerInfo(BaseModel):
    """Information extracted from the user for Airtable registration."""
    name: Optional[str] = Field(None, description="The customer's full name")
    phone: Optional[str] = Field(None, description="The customer's phone number")
    email: Optional[str] = Field(None, description="The customer's email address")
    notes: Optional[str] = Field(None, description="Any specific notes or requests")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

customer_extractor = llm.with_structured_output(CustomerInfo)

template  = """You are the official AI assistant of 'Gökcen Tarım', a professional agricultural supply store.

    Use the provided information to answer the user's question. 
    You have two sources of information:
    1. Technical Documents (Context): {context}
    2. Real-time Price/Stock Data (Airtable): {tool_output}
    3. Chat History: {chat_history}

    Rules:
    1. If there is price or stock information in 'tool_output', prioritize it and state it clearly (e.g., 'Gökcen Tarım'da Üre fiyatı 1.300 TL'dir').
    2. If the answer is not in either source, clearly state that you don't have this specific information but can help with other farming topics.
    3. Your tone should be helpful, professional, and grounded in agricultural expertise.
    4. Keep your response concise (maximum 3-4 sentences).
    5. Always answer in the language the user is speaking.
    6.IMMEDIATELY AFTER stating the price, politely ask if they would like to place an order or be contacted by a representative. 
       If they are interested, ask for their Name and Phone Number.
       (Example: "The price is 1500 TL. Would you like to place an order? If so, please share your Name and Phone number.")
    
    CUSTOMER REGISTRATION TASK:
    - If the user implies they want to register or be contacted, kindly ask for full Name and Phone Number.
    - If they provide details, confirm you received them.
    
    Question:
    {question}
    
    Answer:
    """

gen_prompt = ChatPromptTemplate.from_template(template)

# --- FINAL GENERATION CHAIN ---
generation_chain = gen_prompt | llm | StrOutputParser()