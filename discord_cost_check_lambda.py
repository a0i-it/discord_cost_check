import logging
import json
import urllib
import boto3
import math
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

def trans_usd(cost):

    return math.ceil(float(cost))

def trans_yen(cost):
    url = "https://api.aoikujira.com/kawase/json/usd"
    request=urllib.request.Request(url)
   
    with urllib.request.urlopen(request) as response:
       response_body = json.loads(response.read().decode("utf-8"))
       print(response_body)
    
    return math.ceil(float(cost)*float(response_body['JPY']))
 
### イベントからDiscordメッセージを整形
def parse_event(event):

    client = boto3.client('ce')
    today = datetime.today()

    if (datetime.strftime(today.replace(day=1), '%Y-%m-%d')==datetime.strftime(today, '%Y-%m-%d')):
        message = f"""
        :moneybag: **AWSのコスト通知です** :moneybag:\r
        【算出結果】
        月初日のため処理をスキップしました。
        """
        logger.info('Success Creating Discord Messages!')
        return message
    else:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': datetime.strftime(today.replace(day=1), '%Y-%m-%d'),
                'End': datetime.strftime(today, '%Y-%m-%d')
            },
            Granularity='MONTHLY',
            Metrics=['BlendedCost'],
        )
    
        CostUSD = trans_usd(response['ResultsByTime'][0]['Total']['BlendedCost']['Amount'])
        CostYEN = trans_yen(response['ResultsByTime'][0]['Total']['BlendedCost']['Amount'])

        message = f"""
        :moneybag: **AWSのコスト通知です** :moneybag:\r
        【算出結果】
        ▼算出開始日 : {response['ResultsByTime'][0]['TimePeriod']['Start']}
        ▼算出終了日 : {response['ResultsByTime'][0]['TimePeriod']['End']}
    
        ▼トータル額 : 約{CostUSD} USD
        ▼トータル額 : 約{CostYEN} 円

        """
        logger.info('Success Creating Discord Messages!')
 
        return message
