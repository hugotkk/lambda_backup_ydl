import boto3
from pytube import YouTube
import os
from datetime import datetime
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
import re

patch_all()


def title_to_slug(title):
    slug = title.lower()
    slug = slug.replace(' ', '-')
    slug = re.sub(r'[^\w-]', '', slug)
    slug = slug.strip('-')
    return slug

def lambda_handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']
    for record in event['Records']:
        youtube_url = record['body']
        youtube = YouTube(youtube_url)
        video_id = youtube.video_id
        video_title = title_to_slug(youtube.title)

        # Download video in highest quality MP4 format
        video_stream = youtube.streams.filter(file_extension='mp4').get_highest_resolution()
        filename = f"{video_id} {video_title}.mp4"
        video_stream.download(filename=f"/tmp/{filename}")

        # Create an S3 client
        s3 = boto3.client('s3')

        # Upload the file to S3 in the root partition by date
        date_prefix = datetime.today().strftime('%Y-%m-%d')
        s3_key = f'{date_prefix}/{filename}'
        with open(f"/tmp/{filename}", "rb") as data:
            s3.upload_fileobj(data, bucket_name, s3_key)

        # Delete local file after upload
        os.remove(f"/tmp/{filename}")

    return {
        'statusCode': 200,
        'body': f'Successfully uploaded'
    }

