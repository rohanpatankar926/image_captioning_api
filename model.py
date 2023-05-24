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
import pyttsx3
s3=boto3.resource("s3",aws_access_key_id=getenv("ACCESS_KEY"),aws_secret_access_key=getenv("SECRET_ACCESS_KEY"))
bucket=s3.Bucket(getenv("BUCKET_NAME"))
print(bucket)

app=Flask(__name__)

CORS(app)

#home page
@app.route('/')
def home():
  objects=available_objects()
  return render_template('home.html',objects=objects)

model = VisionEncoderDecoderModel.from_pretrained("jaimin/image_caption")
feature_extractor = ViTFeatureExtractor.from_pretrained("jaimin/image_caption")
tokenizer = AutoTokenizer.from_pretrained("jaimin/image_caption")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}


@app.route("/upload", methods=["POST"])
def upload_img_s3():
    objects=available_objects()
    s3 = boto3.resource("s3", aws_access_key_id=getenv("ACCESS_KEY"), aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))
    try:
        file = request.files['file']
        key=request.form['key']
        if any(obj.key==key for obj in bucket.objects.all()):
            return render_template("home.html",uploaded_message=f'''The key named {key} already exists''',objects=objects)
        encoded_image = base64.b64encode(file.read())
        s3.Bucket(getenv("BUCKET_NAME")).put_object(Key=key, Body=encoded_image)
        uploaded_message=f"{file} uploaded successfully"
        return render_template("home.html",uploaded_message=f'''{uploaded_message.split("'")[1]} uploaded successfully''',objects=objects)
    except Exception as e:
        print(e)
        return "ERROR"


def available_objects():
    try:
        my_bucket = s3.Bucket(os.getenv("BUCKET_NAME"))
        objects=[obj.key for obj in my_bucket.objects.all()]
        return objects
    except Exception as e:
        print(e)
        return []

@app.route("/predict", methods=['POST'])
def predict_step():
    try:
      objects=available_objects()
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
      engine=pyttsx3.init()
      engine.setProperty('rate', 150)
      engine.say("".join(preds))
      engine.runAndWait()

      return render_template("home.html",prediction="".join(preds),image=img_str,objects=objects)
    except Exception as e:
      return jsonify({'predictions': str(e)})
  
if __name__ == '__main__':
  app.run(debug=True,port=4040,host="0.0.0.0")