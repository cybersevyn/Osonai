# Osonai
is a lightweight, cross-platform application designed for Mac and Linux.  
It helps you easily manage budgets and capture ideas without clutter — built with Python, Docker, and wrapped using Platypus to feel like a true native app that stays docked on your launcher.

---

## ✨ Features
- Minimalist budgeting tracker: organize income and expenses
- Idea journal: capture thoughts, inspirations, and notes
- Built with a lightweight Python backend
- Dockerized for simple, consistent deployment
- Native `.app` package for Mac and Linux (via Platypus)
- Launches and stays pinned to your system dock
- Clean and distraction-free user experience

---

## 🛠 Setup and Installation

You can run Osonai two ways:

### 1. Run Locally (for Developers)

```bash
git clone https://github.com/cybersevyn/osonai.git
cd osonai
docker build -t osonai .
docker run -p 3000:3000 osonai
