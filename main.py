import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse

# 哔哩哔哩的cookie
cookies = {
    'SESSDATA': 'your_sessdata',
    'bili_jct': 'your_bili_jct',
    'DedeUserID': 'your_dedeuserid',
    'DedeUserID__ckMd5': 'your_dedeuserid_ckmd5',
    'sid': 'your_sid',
}

# 钉钉机器人的Webhook URL和Secret
dingtalk_webhook = 'your_dingtalk_webhook'
dingtalk_secret = 'your_dingtalk_secret'

# 获取当前时间戳和签名
def get_timestamp_and_sign():
    timestamp = str(round(time.time() * 1000))
    secret_enc = dingtalk_secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, dingtalk_secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign

# 获取会员购订单列表
def get_orders():
    url = 'https://show.bilibili.com/api/ticket/order/list?page=0&page_size=10'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    }
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# 发送钉钉通知
def send_dingtalk_message(message):
    timestamp, sign = get_timestamp_and_sign()
    webhook_url = f'{dingtalk_webhook}&timestamp={timestamp}&sign={sign}'
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'msgtype': 'text',
        'text': {
            'content': message
        }
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    return response.status_code == 200

# 检查订单并发送提醒
def check_orders_and_notify():
    orders = get_orders()
    if orders:
        pending_orders = [order for order in orders['data']['list'] if order['status'] == 1]
        if pending_orders:
            order_details = "\n".join(
                [f"订单ID: {order['order_id']}, 项目名称: {order['item_info']['name']}, 订单金额: {order['total_money']/100}元" for order in pending_orders]
            )
            message = f'你有{len(pending_orders)}个待付款的订单，请尽快处理。订单详情如下：\n{order_details}'
            if send_dingtalk_message(message):
                print('钉钉通知发送成功')
            else:
                print('钉钉通知发送失败')
        else:
            print('没有待付款的订单')
    else:
        print('获取订单失败')

# 主程序
if __name__ == '__main__':
    while True:
        check_orders_and_notify()
        time.sleep(60)
