import ollama
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model to use
MODEL_NAME = "gemma:2b"

def get_system_prompt(mode: str, language: str) -> str:
    """
    Generates a system prompt based on the chosen learning mode and language.
    """
    
    # Base persona
    system_prompt = (
        "You are a friendly, helpful, and patient academic tutor. "
        "Your goal is to help students learn effectively. "
    )
    
    # Language specification
    if language.lower() == "hindi":
        system_prompt += "Please provide your answers primarily in Hindi using Devanagari script. Use simple and clear terms. "
    else:
        system_prompt += "Please provide your answers in clear and simple English. "
        
    # Mode specialization
    if mode.lower() == "simple":
        system_prompt += (
            "Explain concepts using the 'Explain Like I'm 10' principle. "
            "Use very simple words, avoids jargon, and use short sentences. "
            "Think of yourself as explaining to a primary school student. "
        )
    elif mode.lower() == "example":
        system_prompt += (
            "Focus heavily on real-life examples and analogies. "
            "For every concept you explain, provide at least one practical, everyday scenario "
            "that helps a student visualize the idea. "
        )
    else: # Normal mode
        system_prompt += (
            "Provide a standard academic explanation. Include a clear definition "
            "followed by a structured explanation. Use bullet points for clarity where appropriate. "
        )
        
    return system_prompt

def get_summary_prompt(language: str) -> str:
    """
    Prompt for summarization tasks.
    """
    if language.lower() == "hindi":
        return "Please summarize the following text in bullet points in Hindi. Highlight key concepts and important terms."
    return "Please summarize the following text into clear bullet points in English. Highlight key concepts and important keywords."

async def ask_llm(messages: list) -> str:
    """
    Calls the local Ollama instance with gemma:2b.
    """
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            options={
                "temperature": 0.5,
                "top_p": 0.9,
            }
        )
        return response['message']['content']
    except Exception as e:
        logger.error(f"Error calling Ollama: {str(e)}")
        return f"Error connecting to local AI engine: {str(e)}. Please make sure Ollama is running."

def format_chat_history(history: list, system_prompt: str, user_query: str):
    """
    Formats the history and current query into a message list for Ollama.
    """
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add history
    for msg in history:
        messages.append(msg)
        
    # Add current query
    messages.append({"role": "user", "content": user_query})
    
    return messages
