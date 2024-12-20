from flask import Blueprint, request, current_app, jsonify, g
from utils import restful, core
from urllib.parse import urlparse

bp = Blueprint("busuanzi", __name__, url_prefix="/busuanzi")


@bp.before_request
def before_request():
    # 设置 CORS 头部
    g.access_expose_headers = "Set-Bsz-Identity"

    # 获取 Authorization 头部
    token_tmp = request.headers.get("Authorization", "")

    if not token_tmp:
        user_identity = core.get_user_identity()
        g.user_identity = user_identity  # 存储用户身份信息
        g.new_token = core.generate_jwt(user_identity)
    else:
        token = token_tmp.replace("Bearer ", "", 1)
        user_identity = core.check_jwt(token)
        if not user_identity:
            user_identity = core.get_user_identity()
            g.user_identity = user_identity  # 存储用户身份信息
            g.new_token = core.generate_jwt(user_identity)
        else:
            g.user_identity = token_tmp


@bp.route("/get_or_set_api", methods=["POST"])
def get_or_set_api():  # put application's code here
    x_bsz_referer = request.headers.get("x-bsz-referer")
    if x_bsz_referer is None:
        return restful.params_error("invalid referer")

    parsed_url = urlparse(x_bsz_referer)
    host = parsed_url.netloc
    path = parsed_url.path
    if host is None or host == "" or "baispace.cn" not in host:
        return restful.params_error("invalid referer")

    result = core.site_count(
        host,
        path,
        g.user_identity,
    )
    return restful.ok("ok", result)


@bp.after_request
def after_request(response):
    if hasattr(g, "new_token"):
        response.headers["Set-Bsz-Identity"] = {g.new_token}
    return response
