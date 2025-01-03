from flask import Blueprint, request, jsonify, current_app
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
    if msg_from:
        for sender in msg_from:
            name = sender.get("name")
            address = sender.get("address")
            logger.info(f"Processing sender: {name} <{address}>")
            # 在这里执行下一步操作，例如发送邮件或其他处理

    logger.info("Received a webhook request successfully.")
    return jsonify({"status": "OK"}), 200
