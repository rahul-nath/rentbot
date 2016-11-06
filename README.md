# Tenant Talk
Tenant Talk is a web app that allows renters to ask questions about rental law and policy so they can better understand their rights when dealing with landlords. The app uses the [Pandora Bots API](https://developer.pandorabots.com/) to respond to user questions.

## Running the App

1. Get API keys from anthony.fumagalli@gmail.com
2. `pip install -r requirements.txt`
3. `python __init.py`
4. Go to `http://0.0.0.0:5000/`

## Updating the Chatbot

1. Get API keys from anthony.fumagalli@gmail.com
2. `npm install`
3. Change the appropriate AIML file and run `pb upload <changed_file>`
4. `pb compile`
5. Test with `pb talk <command>`
