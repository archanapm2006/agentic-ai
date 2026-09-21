# agent_app/services.py

import os
from google import genai
from dotenv import load_dotenv
from .tools import calculate

load_dotenv(override=True)

def run_react_agent(query):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    has_math = any(kw in query.lower() for kw in ['calculate', 'sqrt', 'pow', '+', '-', '*', '/']) or any(c.isdigit() for c in query)
    
    if has_math:
        # 1. Ask Gemini strictly for the Python expression
        extract_prompt = f"Extract ONLY the valid executable Python math expression for this request. Do NOT include words, markdown code blocks, or extra text: {query}"
        expr_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=extract_prompt
        )
        
        # Clean expression
        expr = expr_response.text.strip().replace('`', '').replace('python', '').strip()
        
        # 2. Run local Python tool
        tool_output = calculate(expr)
        
        # 3. Build explicit ReAct trace
        thought = f"Identified mathematical query. Extracted executable expression '{expr}' for local Python execution."
        action = f"calculate(expression='{expr}')"
        observation = f"Python Execution Result -> {tool_output}"
        
        # 4. Formulate final answer
        answer_prompt = f"User asked: '{query}'. The calculation tool returned: '{tool_output}'. Provide a direct final answer."
        final_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=answer_prompt
        )
        final_answer = final_response.text.strip()
        
    else:
        # General knowledge query
        prompt = f"You are a helpful ReAct agent. Answer the user query clearly: {query}"
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        thought = "Analyzed standard informational request."
        action = "Direct LLM Synthesis"
        observation = "Information retrieved successfully."
        final_answer = response.text.strip()

    return {
        "thought": thought,
        "action": action,
        "observation": observation,
        "final_answer": final_answer
    }