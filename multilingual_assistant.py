from flask import Flask, request, jsonify, send_file
from googletrans import Translator
from gtts import gTTS
import tempfile
import os
from gemini_client import ask_gemini

app = Flask(__name__)

@app.route('/api/speak', methods=['POST'])
def speak():
    try:
        # Get data from request
        data = request.json
        user_query = data.get('query')
        lang = data.get('lang', 'hi')  # Default to Hindi
        
        if not user_query:
            return jsonify({"error": "Query parameter is required"}), 400
        
        # Gemini-generated response
        response = ask_gemini(f"Act as a local travel assistant. Answer this: {user_query}")
        
        # Translate to desired language
        translator = Translator()
        translated = translator.translate(response, dest=lang).text
        print(f"[Translated]: {translated}")
        
        # Generate speech
        tts = gTTS(text=translated, lang=lang)
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        temp_file.close()
        
        # Return the audio file
        return send_file(
            temp_file.name,
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name="response.mp3"
        )
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        # Clean up the temporary file
        if 'temp_file' in locals():
            try:
                os.unlink(temp_file.name)
            except:
                pass

if __name__ == '__main__':
    app.run(debug=True)