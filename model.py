from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
import torch
from PIL import Image
import base64
from io import BytesIO
from flask import Flask,render_template,jsonify,request
from flask_cors import CORS
from os import getenv
from dotenv import load_dotenv
load_dotenv()
import boto3
import os

s3=boto3.resource("s3",aws_access_key_id=getenv("ACCESS_KEY"),aws_secret_access_key=getenv("SECRET_ACCESS_KEY"))
bucket=s3.Bucket(getenv("BUCKET_NAME"))
print(bucket)

app=Flask(__name__)

CORS(app)

#home page
@app.route('/')
def home():
  return render_template('home.html')

model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}


@app.route("/upload", methods=["POST"])
def upload_img_s3():
    s3 = boto3.resource("s3", aws_access_key_id=getenv("ACCESS_KEY"), aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))
    try:
        file = request.files['file']
        encoded_image = base64.b64encode(file.read())
        s3.Bucket(getenv("BUCKET_NAME")).put_object(Key=request.form['key'], Body=encoded_image)
        print("uploaded to s3")
        uploaded_message=f"{file} uploaded successfully"
        return render_template("home.html",uploaded_message=f'''{uploaded_message.split("'")[1]} uploaded successfully''')
    except Exception as e:
        print(e)
        return "ERROR"


@app.route("/predict", methods=['POST'])
def predict_step():
    try:
      image_paths = request.form.get('image_paths')
      image_obj=bucket.Object(image_paths).get()['Body'].read()
      image_bytes = base64.b64decode(image_obj)
      i_image = Image.open(BytesIO(image_bytes))
      
      print(i_image)
      if i_image.mode != "RGB":
          i_image = i_image.convert(mode="RGB")

      pixel_values = feature_extractor(images=[i_image], return_tensors="pt").pixel_values
      pixel_values = pixel_values.to(device)

      output_ids = model.generate(pixel_values, **gen_kwargs)
      preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
      preds = [pred.strip() for pred in preds]

      buffer = BytesIO()
      i_image.save(buffer, format="PNG")
      img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
      print(img_str)
      return render_template("home.html",prediction="".join(preds),image=img_str)
    except Exception as e:
      return jsonify({'predictions': str(e)})
  
if __name__ == '__main__':
  app.run(debug=True,port=8130,host="0.0.0.0")