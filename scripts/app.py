from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    print(f"Received command: {data['action']}")
    return jsonify({"status": "success", "action": data['action']})

if __name__ == '__main__':
    app.run(debug=True)