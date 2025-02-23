# Ideation Bot - Idea drought figher, a cli chatbot

A gemini based chatbot with the following features:

1. Context Importing - Import context from other chats, all chats within a project.
2. Retrieve chats as text files for later reference.
3. Text files already contain markdown, just change the extension to .md for formatted view.

### Setup

1. Install Python3.9+ from `python.org`
2. Get your gemini api key from `https://aistudio.google.com/apikey`
3. Clone this repository using `git clone https://github.com/sparky0520/ideation_bot.git` command in your terminal
4. Make a virtual environment `python3 -m venv env`
5. Activate the environment using `source env/bin/activate`
6. Install all packages using `pip install -r requirements.txt`
7. Put your gemini api key in GEMINI_API_KEY attribute in `.env` file
8. Start using by running `python main.py`
