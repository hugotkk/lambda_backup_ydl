import boto3
from pytube import YouTube
import os

def lambda_handler(event, context):
    url = event['url']
    bucket_name = event['bucket_name']

    # Download the video to a local file
    youtube = YouTube(url)
    video = youtube.streams.first()
    filename = video.default_filename
    video.download(filename=filename)

    # Create an S3 client
    s3 = boto3.client('s3')

    # Upload the file to S3
    with open(filename, "rb") as data:
        s3.upload_fileobj(data, bucket_name, filename)

    # Delete local file after upload
    os.remove(filename)

    return {
        'statusCode': 200,
        'body': f'Successfully uploaded {filename} to {bucket_name}'
    }

