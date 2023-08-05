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
    subsegment = xray_recorder.begin_subsegment('Put playlist to queue')
    subsegment.put_metadata('playlist', url)
    playlist = Playlist(url)
    for video_url in playlist.video_urls:
        subsegment = xray_recorder.begin_subsegment('Send youtube url to sqs')
        subsegment.put_metadata('video_url', video_url)
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=video_url
        )
        xray_recorder.end_subsegment()
    xray_recorder.end_subsegment()
    return {
        'statusCode': 200,
        'body': f'Successfully sent {len(playlist.video_urls)} video URLs to {queue_name}'
    }

