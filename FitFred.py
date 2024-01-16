from flask import Flask, request, jsonify
from chat_module import chat_with_rishabh

app = Flask(__name__)

user_sessions = {}

@app.route('/chat', methods=['POST'])
def chat():
    user_id = request.json.get('user_id', '')
    user_input = request.json.get('user_input', '')

    # Get or create a session for the user
    if user_id not in user_sessions:
        user_sessions[user_id] = []

    # Call the chat_with_rishabh function
    response = chat_with_rishabh(user_input, user_sessions[user_id])

    return jsonify({"FitFred": response})

if __name__ == '__main__':
    app.run(debug=True)


#curl -X POST -H "Content-Type: application/json" -d '{"user_input": "whats my bmi"}' http://localhost:5000/chat
