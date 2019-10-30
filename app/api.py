import os
from io import BytesIO

from flask import Blueprint, request, jsonify, current_app as app

from app.util.data_format import data_format
from app.util.db import connection
from app.util.utils import get_random_filename, get_type_name_by_id, get_contact, save_img
from config import config
from log import botLog
from mythread import executor
from push.push import send_group_msg

api = Blueprint("api", __name__, url_prefix='/api/v1')


@api.route('/upload', methods=["POST"])
def get_info():
    has_img = False
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            upload_folder = os.path.join(app.config['UPLOAD_FOLDER'])
            if not os.path.exists(upload_folder):
                os.mkdir(upload_folder)

            filename = "{}.jpg".format(get_random_filename())
            new_file = os.path.join(upload_folder, filename)

            MAX_FILE_SIZE = 1.5 * 1024 * 1024
            bytes_ = BytesIO(file.stream.read())
            file_size = len(bytes_.read())
            MB = file_size/(1024**2)
            botLog.info(f"这次上传的图片大小为{MB:.2f}/MB {file_size}/B")
            if file_size>MAX_FILE_SIZE:
                save_img(bytes_,new_file)
            else:
                save_img(bytes_,new_file,quality=100)
            db_filename = os.path.join("upload", filename)
            has_img = True
        type = request.form["type"]
        content = request.form["content"]
        qq = request.form["qq"]
        we_chat = request.form["we_chat"]
        phone = request.form["phone"]

        # 插入数据库
        try:
            with connection.cursor() as cursor:
                if has_img:
                    sql = "INSERT INTO message(message_type,content,qq,wechat,phone,img_url) VALUES (%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql, (type, content, qq, we_chat, phone, filename))
                else:
                    sql = "INSERT INTO message(message_type,content,qq,wechat,phone) VALUES (%s,%s,%s,%s,%s)"
                    cursor.execute(sql, (type, content, qq, we_chat, phone))
            connection.commit()
            with connection.cursor() as cursor:
                cursor.execute("select last_insert_id() as auto_id")
                auto_increment_id = cursor.fetchone().get("auto_id")
        except:
            connection.rollback()
            return jsonify(ret_code=-1)

        # 转发消息到审核群

        contact = get_contact(qq=qq,we_chat=we_chat,phone=phone)
        if has_img:
            botLog.info("这次上传有图片...")
            msg = data_format(auto_increment_id, get_type_name_by_id(type), content+contact, filename)
        else:
            msg = data_format(auto_increment_id, get_type_name_by_id(type), content+contact)
        # msg = f"图片测试[CQ:image,file=http://127.0.0.1:5000/upload/{filename}]"
        executor.submit(send_group_msg(config.get("JUDGE_GROUP"), message=msg))
        botLog.info(f"类型：{type} qq：{qq} 微信：{we_chat} 电话：{phone} \n内容：{content}")

        return jsonify(ret_code=200)
