# biliticket-orderlist-remind

检测B站会员购订单是否有未支付订单的脚本。如果有未支付订单，脚本会及时通过钉钉机器人发送提醒通知。

# 主要功能

## 获取会员购订单列表:

使用哔哩哔哩的API获取会员购订单列表。

## 检查未支付订单:

检查订单列表中是否有未支付订单（状态为1）。

## 发送钉钉通知:

通过钉钉机器人发送未支付订单的提醒通知，包括订单ID、项目名称和订单金额。



# 安装与使用

## **配置Cookie和钉钉Webhook及Secret**: 

修改 `main.py` 文件中的 `cookies`、`dingtalk_webhook` 和 `dingtalk_secret` 变量，填入你自己的哔哩哔哩Cookie和钉钉Webhook URL及Secret。

