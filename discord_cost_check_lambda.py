import logging
import json
import urllib
import boto3
from datetime import datetime, date, timedelta
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
def lambda_handler(event, context):
    try:
        print(event)
        messages = parse_event(event)
        web_hook(messages)
        return {
            'statusCode': 200,
            'body': 'Success Sending Discord'
        }
    except Exception as e:
        logger.exception(e)
        raise e
 
# webhookでDiscordに送信
def web_hook(messages):
    url = "https://discord.com/api/webhooks/XXXXXXXXXXXX"
    method = "POST"
    headers = {"Content-Type" : "application/json"}
    obj = {"content" : messages}
    json_data = json.dumps(obj).encode("utf-8")
    request = urllib.request.Request(
        url,
        json_data,
        {"User-Agent": "curl/7.64.1", "Content-Type" : "application/json"},
        method
    )
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        print(response_body)

 
### イベントからDiscordメッセージを整形
def parse_event(event):

    client = boto3.client('ce')
    today = datetime.today()

    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': datetime.strftime(today.replace(day=1), '%Y-%m-%d'),
            'End': datetime.strftime(today, '%Y-%m-%d')
        },
        Granularity='MONTHLY',
        Metrics=['BlendedCost'],
    )

    message = f"""
    :moneybag: **AWSのコスト通知です** :moneybag:\r
    【算出結果】
    ▼算出開始日 : {response['ResultsByTime'][0]['TimePeriod']['Start']}
    ▼算出終了日 : {response['ResultsByTime'][0]['TimePeriod']['End']}
    
    ▼トータル額 : {response['ResultsByTime'][0]['Total']['BlendedCost']['Amount']} USD

    """
    logger.info('Success Creating Discord Messages!')
 
    return message