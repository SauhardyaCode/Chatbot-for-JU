from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/data/flavours', methods=['GET'])
def home():
    return jsonify(
        {
            "flavours": [
                "vanilla",
                "chocolate",
                "mango"
            ]
        })


if __name__ == "__main__":
    app.run(debug=True,host="localhost",port=5000)