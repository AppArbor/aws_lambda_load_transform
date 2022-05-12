import xml.etree.ElementTree as ET
import json
import urllib.parse
from pathlib import Path
from datetime import datetime

tree = ET.parse('input1.xml')
root = tree.getroot()

def tranfrom_handler():
    parent_map = dict((c, p) for p in tree.iter() for c in p)
    for child in root.findall(".//TrackingMessages"):
       parent = parent_map[child]
       parent.remove(child)
    tree.write('output1.xml')
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    # Get the object from the event and show its content type
    try:
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        source_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
        print(source_bucket)
        print(source_key)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
def test_condition():
    if not ("/" in "TruckerTools-Schneider-30281224615.xml"):
        print("true")
    else:
        print("false")
def test_write():
    tree1 = ET.parse('input1.xml')
    root1 = tree1.getroot()
    xml_str = ET.tostring(root1, encoding='unicode', method='xml')
    print(xml_str)
def test_filename():
    source_key = "TruckerTools-Schneider-30281224615.xml"
    filename_out = "{}-{}.xml".format(Path(source_key).with_suffix(''),datetime.now().strftime("%Y%m%d%H%M%S"))
    print(filename_out)
test_filename()
    
