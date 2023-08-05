import boto3
from pytube import Playlist
import os
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

def lambda_handler(event, context):
    url = event['url']
    queue_name = os.environ['QUEUE_NAME']
    sqs = boto3.client('sqs')
    queue_url = sqs.get_queue_url(QueueName=queue_name)['QueueUrl']
    playlist = Playlist(url)
    for video_url in playlist.video_urls:
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=video_url
        )
    return {
        'statusCode': 200,
        'body': f'Successfully sent {len(playlist.video_urls)} video URLs to {queue_name}'
    }

