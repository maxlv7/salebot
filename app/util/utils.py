import random
import time

from PIL import Image

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
        "10004": "失物招领",
        "10005": "寻物启事",
        "10006": "出租",
        "10007": "求租",
        "10008": "吐槽",
        "10009": "留言",
        "10010": "分享",
        "10011": "交友)",
        "10012": "回复",
        "10013": "兼职",
        "10014": "招聘",
        "10015": "表白",
        "10016": "代取快递",
        "10017": "需代ke",
        "10018": "可代ke",
        "10019": "需代qin",
        "10020": "可代qin",
    }
    return type_dict.get(type_id)


def to_online_pic(img_name: str):
    return img_config.get("plugin_get_img_url") + img_name


def get_contact(qq, we_chat, phone):
    msg = "\n"
    if qq != "" and qq != None:
        msg+=f"qq:{qq}\n"
    if we_chat != "" and we_chat != None:
        msg+=f"微信:{we_chat}\n"
    if phone != "" and phone != None:
        msg+=f"手机:{phone}\n"
    return msg

def save_img(bytes, file_path,quality=50):
    im = Image.open(bytes)

    mode_list = ['1', 'L', 'I', 'F', 'P', 'RGB', 'RGBA', 'CMYK', 'YCbCr']
    if im.mode in mode_list:
        im = im.convert('RGB')
    # subsampling=0
    im.save("{}".format(file_path), 'jpeg', quality=quality)