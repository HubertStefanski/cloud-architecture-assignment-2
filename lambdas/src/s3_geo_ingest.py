import json
import urllib
import boto3
from exif import Image

# The code above is an AWS Lambda adapted version of
# https://stackoverflow.com/questions/64113710/extracting-gps-coordinates-from-image-using-python

codec = 'ISO-8859-1'  # or latin-1

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
inventoryTable = dynamodb.Table('AppGeoData')


def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == 'W':
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def image_coordinates(image_path):
    coords = None
    with open(image_path, 'rb') as src:
        img = Image(src)
    if img.has_exif:
        try:
            coords = (decimal_coords(img.gps_latitude,
                                     img.gps_latitude_ref),
                      decimal_coords(img.gps_longitude,
                                     img.gps_longitude_ref))
        except AttributeError:
            print('No Coordinates')
    else:
        print('The Image has no EXIF information')

    return coords


def lambda_handler(event, context):
    # Retrieve new JPG from ingest bucket
    print(f"Event {json.dumps(event, indent=2)}")
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    filename = '/tmp/key.jpg'  # obviously one of your own pictures
    try:
        s3.meta.client.download_file(bucket, key, filename)
    except Exception as e:
        print(e)
        print(
            f'Error getting object {key} from bucket {bucket}. Make sure they exist and your bucket is in the same '
            f'region as this function.')
        raise e

    # Retrieve coords from JPG
    coords = image_coordinates(filename)
    if coords:
        try:
            inventoryTable.put_item(
                Item={
                    'geolocation_lat': str(coords[0]),
                    'geolocation_lng': str(coords[1]),
                    's3_key': key,
                })
        except Exception as e:
            print(e)
            print("Unable to insert data into DynamoDB table".format(e))

    # Move to storage bucket upon completion
    s3.meta.client.copy({'Bucket': bucket, 'Key': key}, "cloud-architecture-geo-data-storage", key)
