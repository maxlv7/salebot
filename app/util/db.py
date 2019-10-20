import pymysql.cursors

from config import db_config
connection = pymysql.connect(**db_config,cursorclass=pymysql.cursors.DictCursor)

# try:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO message(message_type,content,qq,wechat,status)  VALUES ('10001','content','qq','wechat','1') "
#         r = cursor.execute(sql)
#         print(r)
#
#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()
#
#     # with connection.cursor() as cursor:
#     #     # Read a single record
#     #     sql = "SELECT message.qq,type_name FROM `message`,message_type WHERE message.message_type=message_type.message_type"
#     #     cursor.execute(sql)
#     #     result = cursor.fetchall()
#     #     print(result)
# finally:
#     connection.close()
# print()