# 🖍️ Shin-chan's AI Sketchbook

A playful, interactive Streamlit application where you can chat with **Shin-chan** or his alter-ego, **Action Kamen**! Draw pictures for Shin-chan to earn Chocobi points and get mischievous AI feedback.

## ✨ Features
- **Dual Personas:** Toggle "Action Kamen Mode" for a heroic justice-filled experience or stay in "Shin-chan Mode" for mischief and Chocobi.
- **Interactive Sketchbook:** Use a digital canvas to draw for Shin-chan.
- **AI-Powered Chat:** Powered by Ollama (Gemma) to provide authentic, funny responses.
- **Dynamic UI:** The theme changes colors and animations based on the active mode.

---

## 🚀 Steps to follow

### 1. Prerequisites
You must have [Ollama](https://ollama.com/) installed and running on your local machine.
Once Ollama is installed, pull the models used in the app:

ollama pull gemma3:latest

### 2. Installation
Clone this repository and navigate to the project folderthen install the required Python packages:

git clone <repo_link>
cd shinchan-ai-sketchbook
pip install -r requirements.txt

### 3. Running the App
Start the Streamlit server:

streamlit run shinchan.py

---

## 🛠️ Built With

Streamlit - The fastest way to build and share data apps.
Ollama - Local LLM integration.
Streamlit Drawable Canvas - For the drawing interface.
