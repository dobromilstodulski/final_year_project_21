import boto3
from uuid import uuid4
import os
from flask import current_app as app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
  
         
def make_unique(string):
    ident = uuid4().__str__()
    return f"{ident}-{string}"
           

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

s3_resource = boto3.resource("s3")

    
def upload_file(file):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        s3.upload_fileobj(
            file,
            os.getenv("AWS_BUCKET_NAME"),
            file.filename,
            ExtraArgs={
                "ContentType": file.content_type    #Set appropriate content type as per the file
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "{}{}".format(os.getenv("AWS_DOMAIN"), file.filename)


def delete_file(file):
    try:
        s3.delete_object(Bucket=os.getenv("AWS_BUCKET_NAME"), Key=file)
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "file deleted."