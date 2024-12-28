import hashlib
import jwt
from flask import current_app, request
from exts import redis
import requests
from PIL import Image
from io import BytesIO
import numpy as np
from sklearn.cluster import KMeans
import secrets


def get_user_identity():
    client_ip = request.remote_addr
    if "X-Forwarded-For" in request.headers:
        client_ip = request.headers["X-Forwarded-For"].split(",")[0]  # 取第一个 IP
    user_agent = request.headers.get("user-agent")
    return hashlib.md5((client_ip + user_agent).encode()).hexdigest()


def generate_jwt(user_identity):
    # return jwt.encode(
    #     {"identity": user_identity},
    #     current_app.config["BUSUANZI_JWT_SECRET_KEY"],
    #     algorithm="HS256",
    # )
    sign = sha256_hash(user_identity, current_app.config["BUSUANZI_JWT_SECRET_KEY"])
    return f"{user_identity}.{sign}"


def sha256_hash(text: str, salt: str) -> str:
    """
    使用SHA1生成哈希值（注意：原函数使用的是SHA1，而非SHA256）

    :param text: 待哈希的文本
    :param salt: 盐值
    :return: 十六进制格式的哈希字符串
    """
    # 创建SHA1哈希对象
    hasher = hashlib.sha1()

    # 更新哈希对象
    hasher.update(text.encode("utf-8"))
    hasher.update(salt.encode("utf-8"))

    # 获取哈希摘要并转换为十六进制字符串
    return hasher.hexdigest()


def check_jwt(token):
    # try:
    #     decoded = jwt.decode(
    #         token, current_app.config["BUSUANZI_JWT_SECRET_KEY"], algorithms=["HS256"]
    #     )
    #     return decoded.get("identity")
    # except jwt.ExpiredSignatureError:
    #     return ""
    # except jwt.InvalidTokenError:
    #     return "
    """
    验证token
    :param token: 待验证的token
    :return: 如果验证成功返回用户标识，否则返回空字符串
    """
    # 分割token
    parts = token.split(".")

    # 检查token格式
    if len(parts) != 2:
        return ""

    # 验证签名
    user_identity, provided_sign = parts
    calculated_sign = sha256_hash(
        user_identity, current_app.config["BUSUANZI_JWT_SECRET_KEY"]
    )

    # 安全比较签名
    if secrets.compare_digest(calculated_sign, provided_sign):
        return user_identity

    return ""


def site_count(host, path, user_identity):
    rk = get_redis_keys(host, path)

    # sitePV 和 pagePV 使用 String / Zset 存储
    site_pv = redis.incr(rk.get("site_pv_key"))
    page_pv = redis.zincrby(rk.get("page_pv_key"), 1, rk.get("path_unique"))

    user_identity = str(user_identity)
    print(
        f"user_identity: '{user_identity}' - type: {type(user_identity)} - encoded: {user_identity.encode('utf-8')}"
    )

    # siteUv 和 pageUv 使用 HyperLogLog 存储
    redis.pfadd(rk.get("site_uv_key"), user_identity)
    redis.pfadd(rk.get("page_uv_key"), user_identity)

    # 统计 siteUv 和 pageUv
    site_uv = redis.pfcount(rk.get("site_uv_key"))
    page_uv = redis.pfcount(rk.get("page_uv_key"))

    return {
        "site_pv": site_pv,
        "site_uv": site_uv,
        "page_pv": int(page_pv),
        "page_uv": page_uv,
    }


def get_redis_keys(host, path):
    site_unique = hashlib.md5(host.encode()).hexdigest()
    path_unique = hashlib.md5(path.encode()).hexdigest()

    redis_prefix = "bsz"  # 更换为实际的 Redis 前缀

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


def get_image_color(image_url):
    # 下载图片
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # 将图片转换为 RGB 模式（如果不是的话）
    img = img.convert("RGB")

    # 调整图片大小以加快处理速度
    img = img.resize((100, 100))

    # 将图片转换为数组
    img_array = np.array(img)

    # 确保数组的形状是 (n_pixels, 3)
    img_array = img_array.reshape(-1, 3)  # 变为 (n_pixels, 3)

    # 使用 KMeans 聚类获取主题色
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(img_array)

    # 获取聚类中心（主题色）
    colors = kmeans.cluster_centers_

    # 返回主题色（取第一个聚类中心的颜色）
    dominant_color = colors[0].astype(int)  # 转换为整数
    return tuple(dominant_color)


def rgb_to_hex(rgb):
    return "#" + "".join(f"{int(c):02x}" for c in rgb)


def calculate_md5(input_string):
    # 创建 MD5 哈希对象
    md5_hash = hashlib.md5()

    # 更新哈希对象以包含输入字符串的字节
    md5_hash.update(input_string.encode("utf-8"))

    # 获取十六进制的哈希值
    return md5_hash.hexdigest()
