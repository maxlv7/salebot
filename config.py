import os

config = {
    # 机器人QQ
    "MASTER": "2684692286",
    # 审核群
    "JUDGE_GROUP": "644919551",
    # 用户群
    "PUSH_GROUP": ["666902169",
                   "821822935",
                   "622080940",
                   "669065596",
                   "928290072",
                   "364273302",
                   "640544764"
                   ],
    # 上传图片路径
    "UPLOAD_FOLDER": os.path.join(os.path.abspath(os.path.dirname(__file__)), "upload")
}
img_config = {
    # 机器人提交图片地址(也就是后端所在IP)
    "plugin_get_img_url": "http://120.78.216.241:5000/upload/"
}
db_config = {
    # 数据库ip
    "host": "127.0.0.1",
    # 数据库用户名
    "user": "sale_bot",
    # 数据库名称
    "db": "sale_bot",
    # 数据库密码
    "password": "G6S78NYBmKhxMAxc",
    # 端口
    "port": 3306,
    # 编码
    "charset": 'utf8mb4',
}
# 机器人所在的ip
base_bot_url = "http://139.196.98.165:5700"
msg_config = {
    "send_group_msg": f"{base_bot_url}/send_group_msg"
}
redis_config = {
    # redis ip
    "host": "127.0.0.1",
    # redis 端口
    "port": 6379,
    # 数据库名
    "db": 0
}
