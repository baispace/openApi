from flask import Blueprint, request, jsonify, current_app
import requests
from exts import logger
import json
from bs4 import BeautifulSoup
import re


bp = Blueprint("ct24h", __name__, url_prefix="/ct24h")


@bp.route("/webhook/<string:signature>", methods=["POST"])
def webhook(signature):
    # 获取请求体
    request_body = request.get_data(as_text=True)

    # 日志记录请求信息
    logger.info("Received a webhook request.")

    # 获取请求体中的 JSON 数据
    data = request.json
    # logger.info(f"Request data: {data}")

    # 验证签名
    if signature not in [current_app.config["WEBHOOK_TOKEN"]]:
        logger.error("Invalid signature.")
        return jsonify({"error": "Unauthorized"}), 403

    # 解析 JSON 数据
    try:
        data = json.loads(request_body)
    except json.JSONDecodeError:
        logger.error("Invalid JSON format.")
        return jsonify({"error": "Invalid JSON format"}), 400

    # 提取需要的信息
    subject = data.get("subject", "")
    body = data.get("body", "")
    plain_text = data.get("plain_text", "")

    # 将富文本内容转换为纯文本
    body_text = remove_urls(convert_html_to_text(body))

    # 格式化消息内容
    message_content = (
        f"主题: {subject}\n\n内容:\n{body_text}\n\nプレーンテキスト:\n{plain_text}"
    )

    # 解析 msg_from 字段
    msg_from = data.get("msg_from", [])
    if msg_from:
        for sender in msg_from:
            # name = sender.get("name")
            address = sender.get("address")
            # 在这里执行下一步操作，例如发送邮件或其他处理
            if address in ("security@facebookmail.com"):
                send_wechat_notification(message_content)
    return jsonify({"status": "OK"}), 200


def send_wechat_notification(message_content):
    # 构建企业微信消息
    message = {
        "msgtype": "text",
        "text": {"content": message_content},
    }

    # 企业微信 Webhook URL
    wechat_webhook_url = (
        "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="
        + current_app.config["WECHAT_WEBHOOK_TOKEN"]
    )

    # 发送 POST 请求到企业微信 Webhook
    response = requests.post(wechat_webhook_url, json=message)
    if response.status_code != 200:
        logger.error(f"Failed to send notification: {response.text}")
    else:
        logger.info(f"Notification sent to WeChat successfully. {message_content}")


def convert_html_to_text(html_content):
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, "lxml")
    # 找到所有链接并删除
    for a in soup.find_all("a"):
        a.decompose()  # 删除链接标签

    # 提取文本
    text = soup.get_text(separator="\n", strip=True)

    # 使用正则表达式去除所有域名链接
    text = re.sub(r"https?://[^\s]+|www\.[^\s]+", "", text)

    return text.strip()


def remove_urls(text):
    # 使用正则表达式去除所有 URL
    return re.sub(r"https?://[^\s]+", "", text)
