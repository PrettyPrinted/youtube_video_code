import boto3

from flask import Flask, render_template, request
from botocore.config import Config 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/uppy/s3")
def uppy_s3():
    s3_client = boto3.client("s3", "us-east-2", config=Config(signature_version="v4"))

    url = s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": "onemoretestbucket", "Key": "uppyfile.pdf", "ContentType": "application/pdf"},
        ExpiresIn=3600
    )

    return {
        "method": "PUT",
        "url": url,
        "headers": {
            "content-type": "application/pdf"
        }
    }