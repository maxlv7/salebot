import requests

from config import msg_config
from log import botLog

headers = {
    'Content-Type': 'application/json',
    'Connection': 'close',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Mobile Safari/537.36',

}


def send_group_msg(group_id, message, auto_escape=False):
    data = {
        "group_id": group_id,
        "message": message,
        "auto_escape": auto_escape
    }
    res = requests.post(msg_config.get("send_group_msg"), json=data)
    if res.json().get("status") == "ok":
        botLog.info(f"转发到{group_id}---{message[:10]}成功!")
    else:
        botLog.info(f"转发到{group_id}---{message[:10]}失败!")


if __name__ == '__main__':
    send_group_msg("157777470", "test")
