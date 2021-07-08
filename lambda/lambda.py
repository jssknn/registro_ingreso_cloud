import datetime as dt
import boto3
import urllib.parse
import re

# boto3 S3 initialization
s3_client = boto3.client("s3")

def detect_text(photo, bucket):

    client=boto3.client('rekognition')

    response=client.detect_text(Image={'S3Object':{'Bucket':str(bucket),'Name':str(photo)}})
                        
    textDetections=response['TextDetections']
    detecciones = []
    for text in textDetections:
            
        if text['DetectedText'].isupper() and len(text['DetectedText']) > 5 and len(text['DetectedText']) < 10 and re.search("\d{3}", text['DetectedText']):
            detecciones.append(text['DetectedText'].replace(" ", ""))
    
    return detecciones[0] if len(detecciones) != 0 else "NO DETECTABLE"

def put_item_db(fecha, patente):
    dynamodb = boto3.client('dynamodb')
    dynamodb.put_item(TableName='fotos', Item={'fecha':{'S':fecha},'patente':{'S':patente}})        
    
def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:

        dt_string = (dt.datetime.now() - dt.timedelta(hours=3) ).strftime("%d/%m/%Y %H:%M:%S")
        print(key, bucket)
        texto=detect_text(key, bucket)
        put_item_db(dt_string, str(texto))
        return dt_string, str(texto)
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e    
        