from flask import Flask, jsonify, request
from flask_cors import CORS
import bot as BotBrain

app = Flask(__name__)
CORS(app)
bot = BotBrain.GeneralFunctions()
bot.activateBot()

@app.route('/data/message', methods=['POST'])
def receive_message():
    data = request.get_json()
    query = data['message']
    if (query == "${Restart_Assistant}"):
        bot.restart()
    else:
        print(f"Received message: {query}")

    # try:
    response = bot.reply(query)
    return jsonify({"reply": response})
    # except Exception as e:
    #     print("Error:",e)
    #     return jsonify({"reply": "Sorry we ran into some INTERNAL SERVER ERROR! Please reload the page or try again later"})


if __name__ == "__main__":
    app.run(debug=True,host="localhost",port=5000)