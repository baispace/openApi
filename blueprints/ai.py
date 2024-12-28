from flask import Blueprint, request, current_app
from utils import restful
from openai import OpenAI
from urllib.parse import urlparse
from exts import redis

bp = Blueprint("ai", __name__, url_prefix="/ai")


@bp.route("/summary", methods=["POST"])
def get_ai_summary():  # put application's code here
    referer = request.referrer
    if referer is None or "baispace.cn" not in referer:
        return restful.params_error("不被允许的站点")

    data = request.get_json()  # 获取 JSON 数据
    url = data.get("url")
    content = data.get("content")

    if url is None or content is None:
        return restful.params_error("参数不能为空")

    parsed_url = urlparse(url)
    article_path_key = "blog:" + parsed_url.path
    model_reply = redis.get(article_path_key)

    if model_reply is not None:
        return restful.ok("ok", {"summary": model_reply})

    try:
        ali_client = OpenAI(
            api_key=current_app.config["ALI_API_KEY"],
            base_url=current_app.config["ALI_API_URL"],
        )
        promote = "你是一个摘要生成工具，请根据我发送的内容生成一段不超过300字的简洁中文摘要，请直接回答这篇文章讲述了什么。摘要应不包含任何链接，并且仅限于描述文章的主要内容，无需提出建议或指出缺失的部分，也不需要提及用户。"
        completion = ali_client.chat.completions.create(
            model="qwen-turbo",
            messages=[
                {"role": "system", "content": promote},
                {"role": "user", "content": content},
            ],
        )
        model_reply = completion.choices[0].message.content
        # 设置缓存，过期时间7
        redis.set(article_path_key, model_reply, timeout=60 * 60 * 24 * 7)
    except Exception as e:
        return restful.server_error(e)

    return restful.ok("ok", {"summary": model_reply})
