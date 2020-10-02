#!/usr/bin/env python3
# coding: utf-8
from io import BytesIO
from flask import Flask, request
from PIL import Image, ImageOps

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello():
    img = Image.open(BytesIO(request.data))
    return 'image size: ({}, {})\n'.format(img.size[0], img.size[1])


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
