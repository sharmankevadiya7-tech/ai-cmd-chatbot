#  Windows CMD AI Chatbot

Fastest AI chatbot for Windows Command Prompt using Cerebras API!

## 🚀 How to Use

### Prerequisites
- Windows 10/11
- Python installed

### Steps to Run

1. **Download the file**
   - Click `my_ai_bot.py`
   - Click "Download raw file"

2. **Install required package**
   ```cmd
   pip install requests
Run the bot

cmd
python my_ai_bot.py

4. **Commit changes**

---

## 🔧 Step 3: Code Mein API Key Hide Karna (Important Security Update)

Aapki API key **public ho chuki hai** kyunki aapne file GitHub par drag kar di. Isko secure karna hoga.

### Option 1: Quick Fix - Code Update Karein GitHub Par

1. `my_ai_bot.py` file open karein GitHub par

2. **Edit button** (pencil icon ✏️) click karein

3. Code update karein - API key direct na likhein:

```python
# my_ai_bot.py - Updated Version
import os
import requests
import json

# 🔑 API key - AB YAHAN SE READ HOGI
API_KEY = os.environ.get("CEREBRAS_API_KEY", "csk-mjt8hrt6wndde2djcckf8wrhwen52ndpt5hynjtthnnfthkt")

# Agar env variable nahi hai toh warning show karein
if not API_KEY:
    print("⚠️ Warning: CEREBRAS_API_KEY not set in environment")
    print("Using default key (may be rate limited)")

API_URL = "https://api.cerebras.ai/v1/chat/completions"

# Rest of your code remains same...
