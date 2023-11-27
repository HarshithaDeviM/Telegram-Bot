import telebot, requests, pyjokes, random, os
from random import  shuffle


API_KEY = "6958779225:AAEipILlH9skvasWRIWqss8xMihCWi8D7mo"
GIF_FILENAME = "welcome.gif"
EXCHANGERATE_API_KEY = "fe755983ab841db8f22c3f46"

bot = telebot.TeleBot(API_KEY)
user_answers = {}

@bot.message_handler(commands=['start'])
def start(message):
    gif_path = os.path.abspath(GIF_FILENAME)
    with open(gif_path, 'rb') as gif_file:
        bot.send_animation(message.chat.id, gif_file)
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "I support the following commands: \n /start \n /info \n /help \n /joke \n /meme \n /quiz \n /clearhistory \n /currencyconvert")

@bot.message_handler(commands=['info'])
def info(message):
    bot.reply_to(message, "I am a simple Telegram bot created using the python-telegram-bot library.")

@bot.message_handler(commands=['joke'])
def joke(message):
    # Use pyjokes library for generating jokes
    joke_text = pyjokes.get_joke()
    bot.reply_to(message, joke_text)

@bot.message_handler(commands=['meme'])
def meme(message):
    meme_url = get_random_meme_url()
    bot.reply_to(message, f"Here's a random meme for you:\n{meme_url}")

def get_random_meme_url():
    meme_api_url = "https://api.imgflip.com/get_memes"
    response = requests.get(meme_api_url)

    if response.status_code == 200:
        meme_data = response.json()
        memes = meme_data['data']['memes']
        random_meme = random.choice(memes)
        return random_meme['url']
    else:
        return "Sorry, I couldn't fetch a meme at the moment. Please try again later."


class QuizManager:
    def __init__(self):
        self.quizzes = {}

    def start_quiz(self, user_id):
        response = requests.get("https://opentdb.com/api.php?amount=1&type=multiple")

        if response.status_code == 200:
            quiz_data = response.json()['results'][0]
            question = quiz_data['question']
            options = quiz_data['incorrect_answers'] + [quiz_data['correct_answer']]

            shuffle(options)
            correct_option = options.index(quiz_data['correct_answer']) + 1
            self.quizzes[user_id] = {
                'question': question,
                'options': options,
                'correct_option': correct_option
            }
            user_answers[user_id] = correct_option

            quiz_message = f"{question}\n"
            for i, option in enumerate(options, start=1):
                quiz_message += f"{i}. {option}\n"

            return quiz_message
        else:
            return "Sorry, I couldn't fetch a quiz question at the moment. Please try again later."


quiz_manager = QuizManager()

@bot.message_handler(func=lambda message: message.text.isdigit() and int(message.text) in range(1, 5))
def handle_quiz_answer(message):
    user_id = message.chat.id
    user_answer = int(message.text)

    if user_id in user_answers:
        correct_option = user_answers[user_id]

        if user_answer == correct_option:
            bot.reply_to(message, "Correct! 🎉")
        else:
            bot.reply_to(message, f"Wrong! 😞 The correct answer was option {correct_option}.")
        del user_answers[user_id]
    else:
        bot.reply_to(message, "No active quiz question. Use /quiz to start a new one.")

@bot.message_handler(commands=['quiz'])
def quiz(message):
    user_id = message.chat.id
    quiz_message = quiz_manager.start_quiz(user_id)
    bot.reply_to(message, quiz_message)
    
@bot.message_handler(commands=['clearhistory'])
def clear_history(message):
    user_id = message.chat.id
    if user_id in user_answers:
        del user_answers[user_id]
    bot.reply_to(message, "History cleared successfully.")

def get_conversion_rate(from_currency, to_currency,api_key):
    try:
        api_url = f"https://open.er-api.com/v6/latest/{from_currency}?apikey={api_key}"        
        response = requests.get(api_url)

        if response.status_code == 200:
            exchange_rates = response.json()['rates']
            return exchange_rates.get(to_currency, 1.0)
        else:
            return 1.0
    except requests.RequestException:
        return 1.0

@bot.message_handler(commands=['currencyconvert'])
def convert_currency(message):
    try:
        command_args = message.text.split(' ')
        amount = float(command_args[1])
        from_currency = command_args[2].upper()
        to_currency = command_args[4].upper()

        conversion_rate = get_conversion_rate(from_currency, to_currency,EXCHANGERATE_API_KEY)
        converted_amount = amount * conversion_rate

        bot.reply_to(message, f"{amount} {from_currency} is approximately {converted_amount:.2f} {to_currency}")
    except (IndexError, ValueError):
        bot.reply_to(message, "Invalid command. Please use the /currencyconvert command with the correct format, e.g., '/currencyconvert 10 USD to EUR'.")


print("Hey, I am up....")
bot.polling()
