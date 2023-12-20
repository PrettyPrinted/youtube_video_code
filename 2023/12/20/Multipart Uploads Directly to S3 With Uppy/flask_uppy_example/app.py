import boto3

from flask import Flask, render_template, request
from botocore.config import Config 

app = Flask(__name__)
s3_client = boto3.client("s3", "us-east-2", config=Config(signature_version="v4"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/uppy/s3")
def uppy_s3():
    url = s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": "YOUR-BUCKET", "Key": "uppyfile.pdf", "ContentType": "application/pdf"},
        ExpiresIn=3600
    )

    return {
        "method": "PUT",
        "url": url,
        "headers": {
            "content-type": "application/pdf"
        }
    }

@app.route("/uppy/s3-multipart", methods=["POST"])
def uppy_s3_multipart():
    data = request.get_json()
    content_type = data["type"]
    response = s3_client.create_multipart_upload(Bucket="YOUR-BUCKET", Key="multipartuppyfile.pdf", ContentType=content_type)

    return {
        "uploadId": response["UploadId"],
        "key": response["Key"]
    }

@app.route("/uppy/s3-multipart/<upload_id>", methods=["POST"])
def get_uppy_s3_multi(upload_id):
    data = request.get_json()
    response = s3_client.list_parts(Bucket="YOUR-BUCKET", UploadId=upload_id, Key=data["key"])
    return response["Parts"]

@app.route("/uppy/s3-multipart/<upload_id>/<int:part_number>", methods=["POST"])
def get_uppy_s3_multi_part(upload_id, part_number):
    data = request.get_json()
    url = s3_client.generate_presigned_url("upload_part",
        Params={
            "Bucket": "YOUR-BUCKET", 
            "Key": data["key"],
            "UploadId": upload_id,
            "PartNumber": part_number
        },
        ExpiresIn=3600
    )

    return {"url": url}

@app.route("/uppy/s3-multipart/<upload_id>", methods=["DELETE"])
def delete_uppy_s3_multi(upload_id):
    data = request.get_json()
    s3_client.abort_multipart_upload(Bucket="YOUR-BUCKET", Key=data["key"], UploadId=upload_id)
    return {}

@app.route("/uppy/s3-multipart/<upload_id>/complete", methods=["POST"])
def uppy_s3_multi_complete(upload_id):
    data = request.get_json()
    response = s3_client.complete_multipart_upload(
        Bucket="YOUR-BUCKET",
        Key=data["key"],
        UploadId=upload_id,
        MultipartUpload={"Parts": data["parts"]}
    )
    return {
        "location": response["Location"]
    }