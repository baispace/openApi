from flask import Blueprint, request, jsonify
from utils import restful, core
from exts import redis

bp = Blueprint("tool", __name__, url_prefix="/tool")


@bp.route("/img_rgb", methods=["GET"])
def get_img_rgb():
    referer = request.referrer
    if referer is None or "baispace.cn" not in referer:
        return restful.params_error("不被允许的站点")

    image_url = request.args.get("img")
    if not image_url:
        return restful.params_error("No URL provided")

    image_url_key = "blog:" + core.calculate_md5(image_url)
    hex_color = redis.get(image_url_key)
    if hex_color is not None:
        return jsonify({"RGB": hex_color})

    try:
        rgb_color = core.get_image_color(image_url)
        hex_color = core.rgb_to_hex(rgb_color)  # 转换为 HEX 色号
        # 设置缓存，过期时间7
        redis.setex(image_url_key, 60 * 60 * 24 * 7, hex_color)
        return jsonify({"RGB": hex_color})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
