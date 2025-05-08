# 🧠 Discord Chat Summarizer AI

**Analyze, summarize, and interrogate Discord chat history with surgical precision.**  
This tool leverages state-of-the-art language models from OpenRouter, wrapped in a powerful self-contained UI for fast, accurate insight extraction from conversation logs.

> Developed and optimized by `aerthex` — made for engineers, not tourists.

---

## 🚀 Features

- 🔍 Automatically summarizes the latest **250 messages** of any Discord channel
- 🧠 Maintains **stateful memory** across questions for contextual conversations
- 🤖 Supports **natural language queries** over summarized or raw chat logs
- 🧪 Includes a **live test** for validating OpenRouter API keys
- 🎛️ Configurable via integrated UI: select models, set memory & message limits, reset state
- 🔐 Supports a curated list of **free-tier models** (Qwen, Mistral, LLaMA, DeepSeek, etc.)
- 📦 Persists chat history locally with automatic trimming and compatibility fallback
- 💬 Command interface: `summarize`, `status`, `chat`, and `reset`
- ⚙️ Developed for use with Discord selfbot environments like **Nighty** or similar frameworks

---

## 🧰 Requirements

- Python 3.8+
- [`aiohttp`](https://pypi.org/project/aiohttp/)
- [OpenRouter API key](https://openrouter.ai/keys)

### Installation

```bash
git clone https://github.com/danisqxas/discord-chat-summarizer-ai.git
cd discord-chat-summarizer-ai
pip install -r requirements.txt
```

---

## ⚙️ Project Structure

```
discord-chat-summarizer-ai/
├── chat_summarizer.py         ← Main script (UI + summarization + chat logic)
├── requirements.txt           ← Project dependencies
├── .gitignore                 ← Filters for Python cache, compiled files, and local logs
├── README.md                  ← This document
└── assets/                    ← Reserved for future enhancements or documentation
```

---

## 🛡️ Use Case Scenarios

- **Community Managers:** get summaries of heated discussions, support requests, or feedback threads without reading hundreds of messages.
- **Security Analysts:** log, extract and query Discord communication with forensic context.
- **Bot Developers:** integrate log-awareness and summary systems in your own bots or toolchains.

---

## 📜 License

This project is licensed under the MIT License.  
You’re free to use, modify, or distribute it, but attribution to the original author is expected and appreciated.

---

## 🤝 Credits

- Developed, designed and polished by **aerthex**
- Maintained and published by [@danisqxas](https://github.com/danisqxas)

---

### 🧩 Final Note

> This isn’t just a summarizer — it’s a tool for clarity in chaos.  
> Whether you’re an engineer, community manager or pentester, this script was made to give you control over information overload.  
> If you're looking for quality, it's not in the quantity of code... it's in what it empowers you to do.

> **Built by someone who understands what tools should feel like.**
