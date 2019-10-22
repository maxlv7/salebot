from flask import Flask, request, jsonify
from flask_cors import CORS

from app.util.data_format import data_format_forward
from app.util.db import connection
from app.util.parse_cmd import parse_cmd
from app.util.redis_util import redis_
from app.util.utils import get_contact, get_now_day
from config import config, img_config
from log import botLog
from push.push import send_group_msg

app = Flask(__name__, static_folder="upload")
app.config.update(config)
CORS(app)


@app.route('/test')
def hint():
    return jsonify(status=1, msg="OK")


@app.route('/', methods=["GET", "POST"])
def index():
    res = request.get_json()

    botLog.info(res)
    # 好友消息
    # subtype
    if res.get("message_type") == 'private':
        my_url ="http://120.78.216.241:5000/upload/qrcode.png"
        msg = f"长按识别二维码，然后提交您需要发布的信息。[CQ:image,file={my_url}]"
        return jsonify(reply=msg, auto_escape=False)

    # 群消息
    if res.get("message_type") == 'group':

        if str(res.get("group_id")) == config.get("JUDGE_GROUP"):
            botLog.info(f"消息来自审核群{config.get('JUDGE_GROUP')}")
            cmd = res.get("message")
            botLog.info(f"解析到命令为:{parse_cmd(cmd)}")
            # 解析指令，查找编号，排序
            if len(parse_cmd(cmd)) == 2:
                key, value = parse_cmd(cmd)
                # 转发消息(指定命令)
                if key != "error" or value != -1:
                    # 通过
                    if key=="通过":
                        with connection.cursor() as cursor:
                            sql = "SELECT message_id,status FROM message WHERE message_id=%s"
                            cursor.execute(sql, (value,))
                            result = cursor.fetchone()
                        # 没有此编号
                        if result is None:
                            return jsonify(reply=f"编号<{value}>无效,请核对后发送!")
                        # 有，判断状态
                        msg_id = result.get("message_id")
                        msg_status = result.get("status")
                        botLog.info(f"msg_id:{msg_id} msg_status:{msg_status}")
                        if msg_status == 1:
                            return jsonify(reply=f"编号<{value}>已经转发了!")
                        else:
                            execute_user_id = res.get("user_id")
                            botLog.info(f"操作员是 <{execute_user_id}>")
                            # 查询要发送的消息内容
                            with connection.cursor() as cursor:
                                sql = "SELECT type_name,content,qq,wechat,phone,img_url FROM message,message_type WHERE message.message_type = message_type.message_type and message_id=%s"
                                cursor.execute(sql, (msg_id,))
                                msg_detail = cursor.fetchone()

                                msg_type = msg_detail.get("type_name")
                                content = msg_detail.get("content")
                                qq = msg_detail.get("qq")
                                wechat = msg_detail.get("wechat")
                                phone = msg_detail.get("phone")
                                img_url = msg_detail.get("img_url")
                            # 转发到各群中,并记录操作员的qq
                            with connection.cursor() as cursor:
                                sql = "UPDATE message SET status=1,judge_user=%s WHERE message_id = %s"
                                cursor.execute(sql, (execute_user_id, msg_id))
                            connection.commit()
                            # group_id = res.get("group_id")
                            # TODO redis控制当天发送的编号
                            # 当天时间key
                            now = get_now_day()
                            day_serial_number = redis_.get(now)
                            if day_serial_number is None:
                                botLog.info(f"进入第下一天，新加key....当天是<{now}>")
                                redis_.set(now, "1")
                                day_serial_number = redis_.get(now)
                            contact = get_contact(qq=qq, we_chat=wechat, phone=phone)
                            # 没有图片
                            if img_url is None:
                                msg = data_format_forward(day_serial_number, msg_type, content + contact)
                                redis_.set(now, int(day_serial_number) + 1)
                            else:
                                msg = data_format_forward(day_serial_number, msg_type, content + contact, img_url)
                                redis_.set(now, int(day_serial_number) + 1)
                            for group_id in config.get("PUSH_GROUP"):
                                send_group_msg(group_id=group_id, message=msg)
                    if key=="拒绝":
                        with connection.cursor() as cursor:
                            sql = "SELECT message_id,status FROM message WHERE message_id=%s"
                            cursor.execute(sql, (value,))
                            result = cursor.fetchone()
                        # 没有此编号
                        if result is None:
                            return jsonify(reply=f"编号<{value}>无效,请核对后发送!")
                        # 有，判断状态
                        msg_id = result.get("message_id")
                        msg_status = int(result.get("status"))
                        if msg_status==2:
                            #拒绝
                            with connection.cursor() as cursor:
                                sql = "UPDATE message SET status=0 WHERE message_id=%s"
                                cursor.execute(sql, (msg_id,))
                            connection.commit()
                            return jsonify(reply=f"拒绝编号{msg_id}成功!")

    return jsonify(success=True)


from app.api import api

app.register_blueprint(api)
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
