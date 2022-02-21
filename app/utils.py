import boto3
from uuid import uuid4
import os
from werkzeug.utils import secure_filename
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
    #filename = secure_filename(file.filename)
    #with open(file, 'rb') as data:
    s3.upload_fileobj(
        file,
        os.getenv("AWS_BUCKET_NAME"),
        file.filename,
        ExtraArgs={
            "ContentType": file.content_type
        }
    )
    
def send_to_s3(file, bucket_name):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ContentType": file.content_type    #Set appropriate content type as per the file
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "{}{}".format(os.getenv("AWS_DOMAIN"), file.filename)
        
def upload_file_to_s3(file, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            os.getenv("AWS_BUCKET_NAME"),
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    

    # after upload file to s3 bucket, return filename of the uploaded file
    return file.filename
        
def upload_file_object(file):
    bucket = s3_resource.Bucket(os.getenv("AWS_BUCKET_NAME"))
    obj = bucket.Object(file.filename)
    with open(file, 'rb') as data:
        obj.upload_fileobj(data)
        
        

def upload_object(file):
        filename = secure_filename(file.filename)
        s3.put_object(
            Body=file,
            Bucket=os.getenv("AWS_BUCKET_NAME"),
            Key=file.filename,
            ContentType=file.content_type
        )
        
def upload_file2(file, acl="public-read"):
        s3.upload_file(
            file,
            os.getenv("AWS_BUCKET_NAME"),
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )