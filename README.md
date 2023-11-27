# Telegram-Bot
This is a simple Telegram bot created using the python-telegram-bot library. The bot provides various commands for jokes, memes, quizzes and currency conversion.


 ## Features
/start: Displays a welcome animation.
/help: Lists all available commands.
/info: Provides information about the bot.
/joke: Generates a random joke using the pyjokes library.
/meme: Fetches and displays a random meme from an external API.
/quiz: Starts a quiz with a random question.
/clearhistory: Clears the user's quiz answer history.
/currencyconvert: Converts currency based on the provided exchange rates.

## Getting Started
1. clone the repository:
   ```
   git clone https://github.com/HarshithaDeviM/Telegram-Bot.git
   ```
2. Install Dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up a Telegram bot and obtain the API key.
   - Follow the BotFather instructions to create a new Telegram bot.
   - Note down the generated API token.
4. Replace the placeholder API key (`API_KEY`) in the code with your actual Telegram bot API key.
5. Set up an account on an exchange rate API service and obtain the API key.
6. Replace the placeholder exchange rate API key (`EXCHANGERATE_API_KEY`) in the code with your actual exchange rate API key.

## Run the Bot
1. Run the Bot Script:
   ```
   python Bot.py
   ```
2. Start Chatting:
   - Open Telegram and search for your bot by its username(JesterMate).
   - Start a chat with the bot by clicking the "Start" button.

### Note
```
To ensure continuous 24/7 availability of the bot, you can host it on a cloud-based service. In my case, the bot has been successfully hosted on PythonAnywhere.
``` 
