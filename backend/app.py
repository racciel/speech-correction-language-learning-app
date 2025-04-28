from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from your React frontend

@app.route('/api/correct', methods=['POST'])
def correct_speech():
    data = request.get_json()
    text = data.get('text', '')

    # Dummy correction logic (replace this later!)
    corrected_text = text.replace('wrng', 'wrong')

    return jsonify({'corrected_text': corrected_text})

if __name__ == '__main__':
    app.run(debug=True)
