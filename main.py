import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

def ask_ai_bot(user_message):
    url = "https://text.pollinations.ai/"
    system_instruction = "You are a cool Instagram AI Bot. Always reply in Hindi or Hinglish, and your reply MUST be strictly 1 line only."
    payload = {
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_message}
        ]
    }
    try:
        response = requests.post(url, json=payload)
        return response.text.strip()
    except:
        return "❌ एआई सर्वर अभी बिजी है भाई!"

def generate_ai_image_link(prompt):
    trash_words = ["make a photo of", "make an image of", "image of", "photo of", "draw a", "create a", "की फोटो बनाओ", "बनाओ"]
    clean_prompt = prompt.lower()
    for word in trash_words:
        clean_prompt = clean_prompt.replace(word, "")
    clean_prompt = clean_prompt.strip().replace(" ", "%20")
    return f"https://image.pollinations.ai/prompt/{clean_prompt}"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json or {}
    incoming_message = data.get("message", "")
    
    if any(word in incoming_message.lower() for word in ["photo", "image", "make", "draw", "बनाओ", "create"]):
        reply = f"भाई, आपकी एआई फोटो तैयार है! इस लिंक पर क्लिक करके देखो: {generate_ai_image_link(incoming_message)}"
    else:
        reply = ask_ai_bot(incoming_message)
        
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
