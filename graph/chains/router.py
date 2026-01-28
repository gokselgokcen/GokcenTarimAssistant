import os
from typing import Literal,Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class RouteQuery(BaseModel):
    """
     Route a user query to most relevant datasource.
    """
    datasource: Literal["vectorstore","websearch","airtable","direct_response","chat_history"]= Field(
        ...,
        description="Given a user question choose to route  it websearch, vectorstore,airtable or direct response."
    )
    product_name: Optional[str] = Field(
        None, description="The specific product name if asking for price or stock (e.g., 'Üre', '15.15.15')."
    )
    customer_info: Optional[dict] = Field(
        None, description="Extracted customer info (name, surname, phone) if user wants to be contacted."
    )

llm =ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0)
structured_llm_router=llm.with_structured_output(RouteQuery)


system_instructions="""You are an expert at routing a user question to the correct data source.
The user is asking questions about 'Gökcen Tarım' (an agricultural supply store) or general farming topics.

Use the following criteria to decide the datasource:

1. **'airtable'**: Use this ONLY for:
   - Product prices found in the store .
   - Stock availability checks.
   - **Lead generation or contact requests** (e.g., 'call me', 'save my number', 'I want to register'). 
   *Note: If the user asks for a price of a generic commodity like 'stock market wheat price', use web_search.*
   -If user wants to see all products in stock.
   
   When routing to 'airtable':
- If it's a price/stock query: Extract the exact product name (e.g., 'Üre', '15.15.15', 'AS') into 'product_name'.
- If it's a lead/contact request: Extract 'name', 'surname', and 'phone' into the 'customer_info' dictionary.

2. **'vectorstore'**: Use this for:
   - **Technical Agricultural Knowledge:** Planting charts, fertilizer usage manuals, agronomy advice, seed information .
   - **Company Info:** History, vision, mission, return policies, contact address.
   - Example: 'Domatese ne zaman gübre atılır?', 'Buğday ekim aralığı nedir?', 'Vizyonunuz ne?'.
   
    
    
3. **'chat_history'**: Use this when the message requires MEMORY.

CRITICAL RULES:
- If the user asks about identity, memory, name, past messages, preferences, or earlier context, ALWAYS choose 'chat_history'.
- NEVER route identity-related or memory-related questions to 'direct_response'.

Trigger phrases include (not limited to):
- "my name"
- "what is my name"
- "benim adım ne"
- "ne demiştim"
- "hatırlıyor musun"
- "daha önce"
- "önce"
- "beni tanıyor musun"
- "remember"
- "what did I say"
- "who am I"
 
4. **'web_search'**: Use this for **Live/Dynamic Data**:
   - Weather forecasts (e.g., 'İzmir hava durumu').
   - Current news, government announcements, or subsidies.
   - Real-time commodity market prices (e.g., 'Borsada pamuk fiyatı').
   - Questions about topics NOT covered in standard farming manuals.

5. **'direct_response'**: Use this ONLY if:
- The question does NOT fit any category above.
- The question does NOT require memory.
- It is completely standalone.

   

Output only the datasource name.

Examples:
User: Tell me a joke  
→ direct_response

User: What is AI?  
→ direct_response

---

OUTPUT FORMAT:
Return ONLY one datasource name:
- airtable
- vectorstore
- chat_history
- web_search
- direct_response

Do NOT explain anything.
Do NOT add extra text.



Always prioritize 'airtable' for specific price/stock questions regarding Gökcen Tarım's products.
"""
route_prompt = ChatPromptTemplate.from_messages(

    [
    ("system", system_instructions ),
    ("human", "{question}")
    ]
)

question_router = route_prompt | structured_llm_router

if __name__ == "__main__":
    # Ürün fiyatı soralım ki product_name dolsun
    test_query = "Benim adım ne  ?"
    result = question_router.invoke({"question": test_query})

    print(f"Datasource: {result.datasource}")
    print(f"Product Name: {result.product_name}")  # Burada 'Üre' görmeliyiz