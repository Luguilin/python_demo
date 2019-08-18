
import requests
import json




def get_user_info(driverName):
    url = "https://sbpd.faw-vw.com/workOrder/w/workTask?page=0&size=10&sort=id,desc&s_driverName=" + driverName
    response = requests.get(url)
    if response.status_code != 200:
        return
    json_content = json.loads(response.text)
    data = json_content['data']
    for user_info in data:
        if user_info['driverName'] == driverName:
            # 杨业明  承运商：公交 联系电话：13596425226 执行车辆：吉AB9943

            print("%s	承运商：%s	联系电话：%s	执行车辆：%s" % (
                user_info['driverName'], user_info['carrierName'], user_info['driverPhone'], user_info['plateNumber']))
            # return user_info['cardId']
            return user_info
        else:
            continue
    return None


str1="""杨业明
崔柏松
袁兆东
张大伟
王建
赵立明
张禹
周恩波
卢伟
王哨鸣
张建华
冯义
倪斌"""


user_list = str1.split('\n')
for emp_name in user_list:
    user_info = get_user_info(emp_name)
    if user_info is None:
        continue

# get_user_info("杨业明")