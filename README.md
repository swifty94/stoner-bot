Here’s the updated **README.md** file for your **Stoner Bot** project with proper Markdown syntax:

---

# 🌿 Stoner Bot

**Stoner Bot** is a playful Telegram bot that helps determine your "stoned level" based on a fun and quirky quiz. Answer a series of random, funny questions with "Yes" or "No" and discover your level of stoniness along with an image response.

---

## 🚀 Features

- **Randomized Questions**: A pool of funny and random questions with Yes/No answers.
- **Results with Humor**: Based on your answers:
  - 🟢 **Lайт-наркоша**: Mildly stoned.
  - 🟡 **Середній наркєт**: Mid-level stoner.
  - 🔴 **ТОП ТОРЧ!**: Top-tier stoner.
- **Images with Results**: Each result includes a custom image.
- **Restartable Quiz**: Easily restart the quiz at any time.

---

## 📂 Project Structure

```plaintext
stoner-bot/
│
├── stoner_bot/               # Main bot directory.
│   ├── __init__.py           # Empty file to mark as a package.
│   ├── stoner_bot.py         # Main bot script.
│   └── questions.json        # JSON file containing quiz questions.
├── images/                   # Folder with result images.
│   ├── 420_1.jpg
│   ├── 420_2.jpg
│   └── ...
├── requirements.txt          # List of dependencies.
├── README.md                 # Documentation (this file).
└── .gitignore                # Files/folders to ignore (e.g., venv/).
```

---

## 🛠️ Installation

### Prerequisites

- Python 3.9 or later
- Telegram Bot API token (get one from [BotFather](https://core.telegram.org/bots#botfather))

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/stoner-bot.git
   cd stoner-bot
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Questions**:
   Ensure `questions.json` exists in the `stoner_bot/` folder with your quiz questions.

5. **Add Your Telegram Bot Token**:
   - Replace the placeholder token in `stoner_bot.py` with your token from BotFather.

---

## ▶️ Running the Bot

1. Activate the virtual environment:
   ```bash
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. Start the bot:
   ```bash
   python stoner_bot/stoner_bot.py
   ```

3. Interact with your bot on Telegram.

---

## 🌐 Deploying to PythonAnywhere

1. **Upload Files**:
   - Upload the project files (excluding `venv/`) to your PythonAnywhere account.

2. **Set Up Virtual Environment**:
   ```bash
   python3.9 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Schedule Bot to Run**:
   - Use the PythonAnywhere **Tasks** tab to schedule your bot.

---

## 🔧 Configuration

### `questions.json`
Customize the quiz questions in `questions.json`:
```json
[
    "Do you think cats are plotting to take over the world?",
    "Have you ever tried to teach a fish how to swim?",
    ...
]
```

### Images
Store all images in the `images/` folder with filenames like `420_1.jpg`, `420_2.jpg`, etc.

---

## 📜 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## 🙌 Acknowledgments

Thanks to the **Telegram Bot API** and `python-telegram-bot` library for making this bot possible.

---