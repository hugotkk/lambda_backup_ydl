import re
import logging
import boto3
from botocore.exceptions import ClientError
from subprocess import check_output
import os

def youtube_url_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match

    return youtube_regex_match

def upload_file(file_name, bucket, object_name=None):

    if object_name is None:
        object_name = os.path.basename(file_name)
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def handler(event, context):
    if 'url' in event:
        m = youtube_url_validation(event['url'])
        if m:
            id = m.group(6)
            out = "/tmp/{}.mp4".format(id)
            output = check_output("yt-dlp {} -o '{}'".format(id, out), shell=True)
            if output:
                upload_file(out, "")
            else:
                print(output)

    return {
        "message": "Done!"
    }
