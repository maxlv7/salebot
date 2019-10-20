import random
import time

from config import img_config


def get_random_filename() -> str:
    year = time.localtime(time.time()).tm_year
    month = time.localtime(time.time()).tm_mon
    day = time.localtime(time.time()).tm_mday
    hour = time.localtime(time.time()).tm_hour
    min = time.localtime(time.time()).tm_min
    rnum = random.randint(10000, 99999)
    return "{}{}{}{}{}{}".format(year, month, day, hour, min, rnum)

def get_now_day() -> str:
    year = time.localtime(time.time()).tm_year
    month = time.localtime(time.time()).tm_mon
    day = time.localtime(time.time()).tm_mday
    return "{}-{}-{}".format(year, month, day)

def get_type_name_by_id(type_id: str):
    type_id = str(type_id)
    type_dict = {
        "10001": "出售",
        "10002": "求购",
        "10003": "求助",
        "10004": "吐槽",
        "10005": "兼职",
        "10006": "出租",
        "10007": "求租",
        "10008": "其它",
        "10009": "回复",
        "10010": "代(Ke)",
        "10011": "代(Qin)",
    }
    return type_dict.get(type_id)


def to_online_pic(img_name: str):
    return img_config.get("plugin_get_img_url") + img_name


def get_contact(qq, we_chat, phone):
    msg = "\n----联系方式----\n"
    if qq != "" and qq != None:
        msg+=f"qq:{qq}\n"
    if we_chat != "" and we_chat != None:
        msg+=f"微信:{we_chat}\n"
    if phone != "" and phone != None:
        msg+=f"手机:{phone}\n"

    msg+="----联系方式----"
    return msg