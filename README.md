# 🍳 Leftover Genius
### AI-Powered Kitchen Inventory & Food Waste Management

**Leftover Genius** is an AI-powered kitchen management application designed to help small restaurants, cafeterias, and food businesses manage ingredients more efficiently and reduce food waste.

It tracks kitchen inventory, identifies ingredients approaching their expiry dates, and uses Google's Gemini AI to generate practical preparation recommendations based on available ingredients.

## ✨ Features

- **Kitchen Inventory Management:** Add, view, update, and remove ingredients.
- **Expiry Tracking:** Automatically identify expired ingredients and ingredients that need to be used soon.
- **AI-Powered Preparation Plans:** Generate practical food preparation recommendations using Gemini AI.
- **Smart Ingredient Prioritization:** Encourage the use of ingredients approaching expiry.
- **Manager Approval:** Review AI-generated recommendations before recording ingredient usage.
- **Activity History:** Maintain a record of inventory updates and ingredient usage.
- **Persistent Storage:** Store inventory and activity history using SQLite.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web interface |
| Google Gemini API | AI-powered preparation recommendations |
| SQLite | Persistent inventory and activity storage |
| Pandas | Data handling |

## ⚙️ How It Works

1. The user adds ingredients, quantities, units, and expiry dates.
2. Leftover Genius organizes the inventory and identifies ingredients that need attention.
3. The user requests an AI-powered preparation plan.
4. Gemini analyzes the available inventory and generates practical recommendations.
5. A manager reviews and approves a recommendation.
6. The user records ingredient usage, and the inventory and activity history are updated.

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/saharelahi03/Leftover-Genius.git
cd Leftover-Genius
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install streamlit pandas google-genai
```

### 4. Configure your Gemini API key

Create a folder named `.streamlit` and inside it create `secrets.toml`.

Add:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Replace the placeholder with your own API key.

**Important:** Never upload your API key or `secrets.toml` file to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔐 Security

- API credentials are stored locally using Streamlit secrets.
- Sensitive configuration files are excluded through `.gitignore`.
- The SQLite database is excluded from the public repository.

## 🎯 Project Goal

Food waste is a major challenge for restaurants and food businesses. Ingredients are often forgotten, expire before use, or remain underutilized.

Leftover Genius aims to make kitchen management smarter by combining inventory tracking with AI-powered preparation recommendations.

Its goal is simple:

**Use ingredients smarter. Waste less food. Make better kitchen decisions.**

## 👩‍💻 Project Information

**Project:** Leftover Genius  
**Category:** AI-Powered Business Workflow  
**Repository:** https://github.com/saharelahi03/Leftover-Genius

Built as part of the Vultr Agent Rush hackathon.