import xml.etree.ElementTree as ET
import urllib.parse
import boto3
from boto3.session import Session
from pathlib import Path
from datetime import datetime

# AWSclient Id and secret key replace with correct values
sess = Session('access id', 'secret key', None, 'us-east-1')
s3 = sess.client('s3')
TARGET_PATH = 'transformed/'

def lambda_handler():
    # print("Received event: " + json.dumps(event, indent=2))
    # Get the object from the event and show its content type
    try:
        source_bucket = 'z179' # event['Records'][0]['s3']['bucket']['name']
        source_key = "TruckerTools-Schneider-30281224615.xml" # urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
        if not ("/" in source_key):
            filename_out = "{}-{}.xml".format(Path(source_key).with_suffix(''),datetime.now().strftime("%Y%m%d%H%M%S"))
            response = s3.get_object(Bucket=source_bucket, Key=source_key)
            source_xml = response['Body'].read()
            tree = ET.ElementTree(ET.fromstring(source_xml))
            root = tree.getroot()
            parent_map = dict((c, p) for p in tree.iter() for c in p)
            for child in root.findall(".//TrackingMessages"):
               parent = parent_map[child]
               parent.remove(child)
            # tree.write('outs3.xml')
            out_xml_str = ET.tostring(root, encoding='unicode', method='xml')
            # print(out_xml_str[0, 100])
            # s3_resource = sess.resource('s3')
            # s3_resource.Bucket(source_bucket).Object(TARGET_PATH + filename_out).copy(out_xml_str)
            s3.put_object(Bucket=source_bucket, Key=TARGET_PATH + filename_out, Body=out_xml_str);
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.')
        raise e
lambda_handler()