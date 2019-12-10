from flask import Flask, jsonify
from flask import request
import base64
import ImageSteganography as stego
import cipher_key as text_cipher
import PIL


app = Flask(__name__)

img = None

@app.route('/encode', methods = ['POST'])
def encode():
    try:
        if request.method == 'POST':
            text = request.form.get('text')
            text_to_encode, key = text_cipher.encode_text(str(text).upper())
            print(text_to_encode)
            imageStr = stego.encode_image(text_to_encode).decode('utf-8')
            with open("file.txt","w") as t:
                t.write(imageStr)
            return jsonify({"key" : key, "image":imageStr})
    except:
        return "Error",500

@app.route('/decode', methods = ['POST'])
def decode():
    try:
        try:
            if request.method == 'POST':
                imageStr = request.form.get('image')
                text = stego.decode_image(imageStr)
            try:
                print(text)
                plain_text = text_cipher.originalText(text, request.form.get('key'))
                return jsonify({"text":plain_text})
            except:
                return jsonify({"text":"Key wrong"})
        except:
            return jsonify({"text":"Key Wrong"})
    except:
        return "Error",500

app.run()