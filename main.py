#!/usr/bin/env python3
# coding: utf-8
import requests
from io import BytesIO
from flask import Flask, request

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image, ImageOps

app = Flask(__name__)

LABELS_URL = 'https://s3.amazonaws.com/outcome-blog/imagenet/labels.json'
res = requests.get(LABELS_URL)
labels = {int(key): value for key, value in res.json().items()}

min_img_size = 224
transform_pipeline = transforms.Compose([transforms.Resize((min_img_size, min_img_size)),
                                         transforms.ToTensor(),
                                         transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                              std=[0.229, 0.224, 0.225])])

vgg16 = models.vgg16(pretrained=True)
vgg16.eval()

@app.route('/', methods=['POST'])
def hello():
    img = Image.open(BytesIO(request.data))
    img = transform_pipeline(img)
    img = img.unsqueeze(0)

    with torch.no_grad():
        prediction = vgg16(img)
    pred_label = labels[prediction.data.numpy().argmax()]
    return 'prededted label: {}\n'.format(pred_label)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
