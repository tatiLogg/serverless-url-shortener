import json
import boto3
import string
import random
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def generate_short_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def lambda_handler(event, context):
    print("EVENT DEBUG:", json.dumps(event))  # Helpful for CloudWatch logging
    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON in body"})
        }

    long_url = body.get("longUrl")
    if not long_url:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'longUrl' field"})
        }

    short_id = generate_short_id()
    table.put_item(Item={"shortId": short_id, "longUrl": long_url})

    return {
        "statusCode": 200,
        "body": json.dumps({
            "shortUrl": f"https://your-domain/{short_id}",
            "shortId": short_id
        })
    }
