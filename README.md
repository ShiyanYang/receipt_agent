# 🛒 Grocery Agent

<div align="center">

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)](#)
[![Code Quality](https://img.shields.io/badge/Code%20Quality-Production%20Grade-brightgreen)](#code-quality)

**An AI-powered meal planning and shopping list generation agent**

[Overview](#overview) • [Installation](#installation) • [Usage](#usage) • [Architecture](#architecture) • [Contributing](#contributing)

</div>

---

## 📋 Overview

> **📚 Educational Project** - This is a learning exercise demonstrating production-grade Python development practices, AI integration, and software engineering best practices.

Grocery Agent is an intelligent CLI application that helps users plan meals and generate optimized shopping lists. It uses the Llama language model to:

- 🍽️ Generate multi-day meal plans based on user preferences
- 📝 Maintain a persistent pantry inventory
- 🛍️ Create shopping lists excluding items already in the pantry
- 💾 Remember conversation history for context-aware suggestions

**Built with:** Python • LLaMA • JSON • Production-Grade Best Practices


## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- 5GB+ disk space (for Llama model)
- 8GB+ RAM recommended

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/grocery_agent.git
cd grocery_agent
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download the Llama model** (if not already present)
```bash
mkdir -p models
# Download llama-3-8b-instruct.gguf to models/ directory
# ~4.6GB file from Hugging Face or GGUF repository
```

5. **Set up configuration**
```bash
cp .env.example .env
# Edit .env with your settings (optional - uses defaults)
```

### Basic Usage

**Generate meal plan and shopping list:**
```bash
python main.py
```

**Manage your pantry:**
```bash
python app.py
```

**Available pantry commands:**
```
list              - Show all pantry items
add <item>        - Add item to pantry
remove <item>     - Remove item from pantry
help              - Show help message
quit              - Exit application
```

---

## 📁 Project Structure

```
grocery_agent/
├── agent.py              # Core AI agent implementation
├── pantry.py             # Pantry management and persistence
├── memory.py             # Conversation memory with file storage
├── config.py             # Configuration management (NEW)
├── app.py                # Pantry CLI interface
├── main.py               # Main entry point
├── eval.py               # Evaluation and testing utilities
│
├── data/
│   └── pantry.json       # Pantry items storage
├── memory/
│   └── conversation.json # Conversation history
├── models/
│   └── llama-3-8b-instruct.gguf  # LLM model file
│
├── requirements.txt      # Python dependencies
├── .env.example          # Configuration template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

---

## ⚙️ Configuration

### Environment Variables

Configuration is managed through environment variables with sensible defaults:

```bash
# LLM Settings
export MODEL_PATH="./models/llama-3-8b-instruct.gguf"
export LLM_N_CTX=2048              # Context window size
export LLM_N_THREADS=4             # Number of inference threads
export LLM_TEMPERATURE=0.0         # Generation temperature (0=deterministic)
export LLM_MAX_TOKENS=1024         # Max tokens per response

# Data Storage
export PANTRY_FILE="data/pantry.json"
export MEMORY_FILE="memory/conversation.json"

# Logging
export LOG_LEVEL="INFO"            # DEBUG, INFO, WARNING, ERROR
export ENV="development"           # development, production, testing
```

### .env File (Optional)
Copy `.env.example` to `.env` and customize:
```bash
cp .env.example .env
# Edit .env with your preferred settings
```

See `config.py` for all available options.

---

## 🏗️ Architecture

### Core Components

#### Agent (`agent.py`)
- Orchestrates meal planning and shopping list generation
- Integrates with LLaMA for conversational AI
- Manages ingredient normalization and deduplication

#### Pantry (`pantry.py`)
- Persistent storage of pantry items
- Atomic file operations for data safety
- Input validation and error handling

#### Memory (`memory.py`)
- Conversation history with file persistence
- Search and retrieval capabilities
- Automatic loading on initialization

#### Configuration (`config.py`)
- Centralized configuration management
- Environment variable override support
- Multi-environment profiles (dev, prod, testing)
`

---

## 🧪 Testing & Evaluation

Run the evaluation suite:
```bash
python eval.py
```

This will:
- Generate multiple meal plans
- Measure performance metrics
- Validate output format
- Generate `eval_results.json`


---

## 🐛 Known Limitations

- **LLM Inference Speed** - Depends on model size and hardware
- **Context Limit** - Llama 3 8B has 8K token context window
- **JSON Parsing** - Uses regex-based extraction (not perfect)
- **Concurrent Access** - Single-threaded file access
- **Model Size** - Requires significant disk/memory

See [PRODUCTION_IMPROVEMENTS.md](PRODUCTION_IMPROVEMENTS.md#-remaining-high-priority-issues) for planned improvements.

---
## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📖 Learning Resources

This project demonstrates:
- **Production Python** - Type hints, error handling, logging
- **File I/O** - Atomic operations, JSON persistence
- **AI Integration** - LLaMA model integration, prompt engineering
- **Configuration Management** - Environment variables, config classes
- **Software Architecture** - Modular design, separation of concerns
- **Best Practices** - Code organization, documentation, testing

---

<div align="center">

**Made with ❤️ as a learning exercise**

If you found this helpful, please consider starring ⭐ the repository!

</div>