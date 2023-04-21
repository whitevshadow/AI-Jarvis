import random
import requests



thoughts = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "The only thing we have to fear is fear itself. - Franklin D. Roosevelt",
    "Strive not to be a success, but rather to be of value. - Albert Einstein",
    "It does not matter how slowly you go as long as you do not stop. - Confucius",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston S. Churchill",
    "Happiness is not something ready made. It comes from your own actions. - Dalai Lama",
    "The best way to predict your future is to create it. - Abraham Lincoln",
    "In the end, we will remember not the words of our enemies, but the silence of our friends. - Martin Luther King "
    "Jr.",
]


def thought_day():
    try:
        response = requests.get("https://quotes.rest/qod?category=inspire")
        if response.status_code == 200:
            data = response.json()["contents"]["quotes"][0]
            thought = ("Thought for the day:\n \t" + data["quote"] + "- " + data["author"])
            return thought
        else:
            thought = random.choice(thoughts)
            return thought

    except requests.exceptions.SSLError:
        print("Thoughts error")
