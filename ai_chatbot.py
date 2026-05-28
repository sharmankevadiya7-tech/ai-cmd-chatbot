# advanced_ai_bot.py - Secure Version with Hidden API Key
import os
import requests
import json
import datetime
from dotenv import load_dotenv

# Load API key from .env file (HIDDEN!)
load_dotenv()

# 🔑 API key ab .env file se read hogi - GitHub par visible nahi hogi
API_KEY = os.environ.get("CEREBRAS_API_KEY")

# Check if API key exists
if not API_KEY:
    print("❌ ERROR: API Key not found!")
    print("📝 Please create a .env file with: CEREBRAS_API_KEY=your_key_here")
    print("🔗 Get your free API key from: https://cloud.cerebras.ai")
    input("\nPress Enter to exit...")
    exit(1)

API_URL = "https://api.cerebras.ai/v1/chat/completions"

os.system("title Advanced Cerebras AI Bot")
os.system("color 0E")
os.system("cls")

def show_banner():
    print(""" 
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║     🚀 ADVANCED CEREBRAS AI CHATBOT FOR WINDOWS CMD      ║
    ║                                                          ║
    ║     ⚡ Speed: ~2000 tokens/second                       ║
    ║     💬 Type '/help' for commands                        ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)

def show_help():
    print("""
    📖 Available Commands:
    ====================
    /help     - Show this help menu
    /clear    - Clear screen
    /time     - Show current time
    /exit     - Quit chatbot
    /models   - Show available models
    
    💡 Just type your question to chat with AI!
    """)

def ask_ai(question):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama3.1-8b",
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        print("🤔", end="", flush=True)
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        elif response.status_code == 401:
            return "❌ Invalid API Key! Please check your .env file"
        elif response.status_code == 429:
            return "⏰ Rate limit exceeded! Please wait a moment and try again"
        else:
            return f"❌ Error {response.status_code}: {response.text}"
            
    except requests.exceptions.Timeout:
        return "⏰ Request timeout! Please try again"
    except Exception as e:
        return f"🔌 Connection error: {str(e)}"

# Main program
show_banner()
print("💡 Type '/help' for commands\n")

conversation_history = []

while True:
    try:
        user_input = input("┌──[You] ").strip()
        
        if not user_input:
            continue
        
        # Handle commands
        if user_input.lower() == "/exit":
            print("\n✨ Thanks for chatting! Goodbye! 👋\n")
            break
        
        elif user_input.lower() == "/clear":
            os.system("cls")
            show_banner()
            continue
        
        elif user_input.lower() == "/help":
            show_help()
            continue
        
        elif user_input.lower() == "/time":
            now = datetime.datetime.now()
            print(f"└──> 🕐 Current time: {now.strftime('%H:%M:%S')}")
            continue
        
        elif user_input.lower() == "/models":
            print("""
            📚 Available Free Models:
            ========================
            • llama3.1-8b (Fastest)
            • llama-3.3-70b (Most capable)
            • qwen-3-32b (Multilingual)
            """)
            continue
        
        # Get AI response
        print("┌──[AI Bot] ", end="")
        response = ask_ai(user_input)
        print(f"└──> {response}\n")
        
        # Save to history (optional)
        if len(conversation_history) < 50:  # Limit history size
            conversation_history.append(f"You: {user_input}")
            conversation_history.append(f"AI: {response}")
            
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted! Goodbye!\n")
        break
    except Exception as e:
        print(f"└──> ❌ Unexpected error: {e}\n")
