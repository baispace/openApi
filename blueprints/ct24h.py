from flask import Blueprint, request, jsonify, current_app
import requests
from exts import logger
import json

bp = Blueprint("ct24h", __name__, url_prefix="/ct24h")


@bp.route("/webhook/<string:signature>", methods=["POST"])
def webhook(signature):
    # 获取请求体
    request_body = request.get_data(as_text=True)

    # 日志记录请求信息
    logger.info("Received a webhook request.")

    # 获取请求体中的 JSON 数据
    data = request.json
    logger.info(f"Request data: {data}")

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

    # 解析 msg_from 字段
    msg_from = data.get("msg_from", [])
    msg_to = data.get("msg_to", [])
    if msg_from:
        for sender in msg_from:
            # name = sender.get("name")
            address = sender.get("address")
            # 在这里执行下一步操作，例如发送邮件或其他处理
            if address in ("security@facebookmail.com", "receiver@mail.com"):
                for Toer in msg_from:
                    to_name = Toer.get("name")
                    to_address = Toer.get("address")
                    send_wechat_notification(to_address, to_name)

    logger.info("Received a webhook request successfully.")
    return jsonify({"status": "OK"}), 200


def send_wechat_notification(msg_from, subject):
    # 构建企业微信消息
    message = {
        "msgtype": "text",
        "text": {"content": f"新消息发给: {msg_from}\n标题: {subject}"},
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
        logger.info("Notification sent to WeChat successfully.")
