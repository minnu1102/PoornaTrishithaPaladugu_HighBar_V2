import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

class BaseAgent:
    # UPDATED DEFAULT MODEL BELOW:
    def __init__(self, name, model="gemini-2.5-flash"): 
        self.name = name
        
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=0.0,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            convert_system_message_to_human=True
        )
        self.parser = JsonOutputParser()

    def load_prompt(self, fname):
        try:
            with open(f"prompts/{fname}.md", "r") as f:
                return f.read()
        except FileNotFoundError:
            return "You are a helpful AI assistant. Output JSON."

    def invoke(self, prompt_file, inputs):
        system_text = self.load_prompt(prompt_file)
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_text),
            ("user", "{input}")
        ])
        
        chain = prompt | self.llm | self.parser
        return chain.invoke({"input": str(inputs)})