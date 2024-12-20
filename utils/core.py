import hashlib
import jwt
from flask import current_app, jsonify, request
from exts import cache, redis


def get_user_identity():
    client_ip = request.remote_addr
    if "X-Forwarded-For" in request.headers:
        client_ip = request.headers["X-Forwarded-For"].split(",")[0]  # 取第一个 IP
    user_agent = request.headers.get("user-agent")
    return hashlib.md5((client_ip + user_agent).encode()).hexdigest()


def generate_jwt(user_identity):
    return jwt.encode(
        {"identity": user_identity}, current_app.config["SECRET_KEY"], algorithm="HS256"
    )


def check_jwt(token):
    try:
        decoded = jwt.decode(
            token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
        )
        return decoded.get("identity")
    except jwt.ExpiredSignatureError:
        return ""
    except jwt.InvalidTokenError:
        return ""


def site_count(host, path, user_identity):
    rk = get_redis_keys(host, path)

    # sitePV 和 pagePV 使用 String / Zset 存储
    site_pv = redis.incr(rk.get("site_pv_key"))
    page_pv = redis.zincrby(rk.get("page_pv_key"), 1, rk.get("path_unique"))

    # siteUv 和 pageUv 使用 HyperLogLog 存储
    redis.pfadd(rk.get("site_uv_key"), user_identity)
    redis.pfadd(rk.get("page_uv_key"), user_identity)

    # 统计 siteUv 和 pageUv
    site_uv = redis.pfcount(rk.get("site_uv_key"))
    page_uv = redis.pfcount(rk.get("page_uv_key"))

    return {
        "site_pv": site_pv,
        "site_uv": site_uv,
        "page_pv": page_pv,
        "page_uv": page_uv,
    }


def get_redis_keys(host, path):
    site_unique = hashlib.md5(host.encode()).hexdigest()
    path_unique = hashlib.md5(path.encode()).hexdigest()

    redis_prefix = "busuanzi"  # 更换为实际的 Redis 前缀

    site_uv_key = f"{redis_prefix}:site_uv:{site_unique}"
    page_uv_key = f"{redis_prefix}:page_uv:{site_unique}:{path_unique}"
    site_pv_key = f"{redis_prefix}:site_pv:{site_unique}"
    page_pv_key = f"{redis_prefix}:page_pv:{site_unique}"

    return {
        "site_uv_key": site_uv_key,
        "page_uv_key": page_uv_key,
        "site_pv_key": site_pv_key,
        "page_pv_key": page_pv_key,
        "path_unique": path_unique,
    }
