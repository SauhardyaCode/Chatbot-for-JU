from flask import Flask, jsonify, request
import bot

app = Flask(__name__)

@app.route('/data/message', methods=['POST'])
def receive_message():
    data = request.get_json()
    query = data['message']
    print(f"Received message: {query}")

    try:
        response = bot.search_syllabus(query)
        return jsonify({"reply": response})
    except Exception as e:
        print("Error:",e)
        return jsonify({"error":str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True,host="localhost",port=5000)