import boto3
import urllib
from datetime import datetime

TARGET_BUCKET = 'z10598'
TARGET_PATH = 'loads/'

def lambda_handler(event, context):
    
    # Get incoming bucket and key
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    # Extract filename without path
    filename = "loads{}.csv".format(datetime.now().strftime("%Y%m%d%H%M%S"))
    
    print("Bucket {} key {} input file {} ".format(source_bucket, source_key, filename))
    # Copy object to different bucket
    s3_resource = boto3.resource('s3')
    copy_source = {
        'Bucket': source_bucket,
        'Key': source_key
    }
    s3_resource.Bucket(TARGET_BUCKET).Object(TARGET_PATH + filename).copy(copy_source)
