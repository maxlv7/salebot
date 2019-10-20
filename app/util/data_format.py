from app.util.utils import to_online_pic
from log import botLog


def data_format(id: str, title: str, content: str, img: str = None) -> str:
    if img is None:
        data = \
'''审核编号:【{}】\n标题：{}\n内容：{}\n通过请回复: 通过+编号\n拒绝请回复: 拒绝+编号\n如：通过 1'''.format(id, title, content)
    else:
        data = \
'''审核编号:【{}】\n标题：{}\n内容：{}\n图片: [CQ:image,file={}]\n通过请回复: 通过+编号\n拒绝请回复: 拒绝+编号\n如：通过 1'''.format(id, title, content, to_online_pic(img))
    return data


# 审核成功，转发到指定群
def data_format_forward(sort: str, title: str, content: str, img: str = None) -> str:
    if img is None:
        data = '''{}.【{}】\n{}'''.format(sort, title, content)
    else:
        data = '''{}.【{}】\n{} [CQ:image,file={}]'''.format(sort, title, content, to_online_pic(img))
        botLog.info(f"forward data<<<{data}>>>")
    return data
