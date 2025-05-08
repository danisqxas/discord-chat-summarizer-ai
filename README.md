# 🧠 Discord Chat Summarizer AI

**Summarize, interrogate, and control Discord conversations like a pro.**  
A fully-integrated AI assistant for Discord that fuses conversational intelligence, summarization, and memory into a single self-contained powerhouse — controlled entirely via UI and natural commands.

> ✨ Engineered by `aerthex` — for those who demand clarity, automation, and precision.

---

## 🚀 Key Capabilities

- 📥 **Summarize with a command:** Extract the essence of the last 250 messages in any channel  
- 🧠 **Contextual chat memory:** Persist conversations across turns with dynamic memory pruning  
- 🤖 **Ask anything:** Natural language Q&A about recent logs, summaries, or raw messages  
- 🔐 **Supports multiple models:** DeepSeek, Mistral, Meta-LLaMA, Gemini, Qwen, and more via OpenRouter  
- 🛠️ **Live configuration panel:** Set your API key, choose models, tweak memory — all without touching code  
- 🔬 **Built-in diagnostics:** Instantly test your OpenRouter key from the UI  
- 💬 **Minimal CLI interface:** Use `summarize`, `chat`, `status`, and `reset` directly from Discord  
- 📂 **Auto-persistent state:** Summaries and conversations are trimmed, validated and stored  
- 💾 **Disk-based JSON storage:** Keeps lightweight local logs for sessions  
- 🎛️ **Framework-agnostic:** Designed for use with selfbot environments like Nighty, but portable elsewhere  
- 🧪 **Debug tools included:** Toggle verbose logs when troubleshooting  

---

## 🧠 Why This Exists

Discord is noisy. If you manage communities, monitor logs, or track decisions, context gets buried in a sea of scroll. This project brings structure to that chaos, combining AI summarization with dynamic chat-based interaction. It doesn't just summarize — it understands, remembers, and responds.

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
├── chat_summarizer.py       ← Main script (UI, commands, chat logic, API calls)
├── requirements.txt         ← Dependencies for Python env
├── .gitignore               ← Clean Python artifacts and session files
├── README.md                ← This glorious documentation
└── assets/                  ← Reserved for future enhancements or documentation
```

---

## 📦 Releases

Latest release: **v3.0 — Stable**

```txt
✅ New UI tab with dropdowns, input fields and OpenRouter diagnostics  
✅ Full integration with free-tier OpenRouter models  
✅ Chat memory management with dynamic trimming  
✅ Automatic channel context tracking  
✅ Supports Nighty or compatible Discord selfbot frameworks  
```

Download: [GitHub Releases](https://github.com/danisqxas/discord-chat-summarizer-ai/releases)

Future versions may include:
- Full log export
- Support for multi-channel summaries
- Real-time event tracking

---

## 🔎 Who This Is For

- **Developers** who want real-time insight from logs  
- **Community leads** who moderate large servers  
- **Pentesters** capturing Discord-side communication  
- **Freelancers** automating reports and summaries  
- **People who hate scrolling 4,000 lines of “ok” and “lol”**  

---

## ⚙️ Use Example

Once loaded into your selfbot:

```
<p>summarize                        ← Summarize last 250 messages in this channel  
<p>summarize chat What happened?   ← Ask about events, decisions, or trends  
<p>summarize status                ← View current config: model, memory, summary length  
<p>summarize reset                 ← Clear memory and start fresh  
```

Everything else is handled via UI. It remembers. It prunes. It keeps up.

---

## 🧩 Tech Highlights

- **Resilient local history** with format migration support  
- **Dynamic prompt building** with log summarization and replay  
- **Model-agnostic support**: works with any OpenRouter-compatible model  
- **Adaptive UI**: visible fields, dropdowns, buttons, toasts — all declarative  
- **Futuresafe structure**: easily portable to bot frameworks or API-only versions  

---

## 📜 License

Licensed under the **MIT License** — because code like this should be free and reused with credit.

---

## ✍️ Author

Created and refined by [`aerthex`](https://github.com/danisqxas)  
Maintained and distributed by [@danisqxas](https://github.com/danisqxas)

---

## 🧠 Final Thought

> Most people drown in Discord conversations.  
> This tool lets you breathe — by giving you instant awareness, context-aware chat, and actionable summaries.  
> Whether you're building, moderating or analyzing, _this isn't just a tool — it's an upgrade to how you read chaos._

> **No more endless scrolling. Just clarity. One command away.**
