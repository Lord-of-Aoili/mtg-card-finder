## 📄 README.md

# MTG Card Finder (LLM Edition)

A Python-powered tool for discovering Magic: The Gathering cards using natural language queries, with support for traditional filtering via the Scryfall API. Built on top of a Large Language Model that interprets user intent and maps it to real card attributes—ideal for brewers, theorycrafters, and players who think beyond names and types.

---

## ✨ Features
- 💬 Natural language search using an integrated LLM (e.g. OpenAI, local LLM)
- 🔍 Traditional filters by name, color, type, set, rarity, and more
- 🎯 Intelligent query interpretation ("a white card that draws cards when creatures die")
- 🧠 Prompt engineering pipeline that translates abstract ideas into actionable search criteria
- 📦 Scryfall API integration for real-time card data
- 🖥️ CLI interface, with plans for a conversational web UI

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- `openai` or other LLM-compatible Python client (optional)
- `requests` library

### Installation
```bash
git clone https://github.com/Lord-of-Aoili/mtg-card-finder.git
cd mtg-card-finder
pip install -r requirements.txt
```

### Usage
```bash
python finder.py --query "blue card that punishes overdraw and has a flashback mechanic"
```

Or use structured filters:
```bash
python finder.py --name "Liliana" --type "Planeswalker" --color "Black" --rarity "mythic"
```

### Sample Output
```
Name: Narset, Parter of Veils
Mana Cost: 2U
Type: Legendary Planeswalker — Narset
Rarity: Uncommon
Text: Each opponent can't draw more than one card each turn...
```

---

## 🛠 Planned Features
- Web interface with chat-style prompt support
- Fine-tuned LLM adapter for Scryfall queries
- Card synergy and deck archetype suggestions
- Offline Scryfall mirror and local caching

---

## 🤝 Contributing
Open to feature suggestions and pull requests! If you'd like to help shape how LLMs can be used in card search and curation, please open an issue or reach out.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📬 Contact
Luke Read – [GitHub](https://github.com/Lord-of-Aoili)  
Project Link: https://github.com/Lord-of-Aoili/mtg-card-finder
