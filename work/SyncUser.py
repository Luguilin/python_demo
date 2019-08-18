import requests
import json
import time


def get_user_info(employee_id):
    url = "https://sbpd.faw-vw.com/passenger/w/employeeInformation?" \
          "page=0&size=999&sort=id,desc&s_employeeId=" + employee_id
    response = requests.get(url)
    if response.status_code != 200:
        return
    json_content = json.loads(response.text)
    data = json_content['data']
    for user_info in data:
        if user_info['employeeId'] == employee_id:
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(user_info['lastModifiedDate'] / 1000)))
            print("%s	%s	%s	%s	%s	%s" % (
                user_info['name'], user_info['departmentName'], user_info['employeeId'], user_info['cardId'],
                user_info['telephone'], date))
            # return user_info['cardId']
            return user_info
        else:
            continue
    return None


def delete_user_info(card_id):
    url = "http://device.tjtech.cc/delete?serialNumber=" + card_id
    response = requests.get(url)


def user_sync(user_id):
    response = requests.post("https://sbpd.faw-vw.com/passenger/w/employeeInformation/" + str(user_id))


str1 = """Z036279
8505
1850
27517
Z053628
5520
24376
Z009359
Z043008
Z016116
Z052878
Z052823
Z052842
Z052826
Z052864
Z053633
Z052883
16738
3293
Z037656"""

user_list = str1.split('\n')
for emp_id in user_list:
    user_info = get_user_info(emp_id)
    if user_info is None:
        continue
    delete_user_info(user_info['cardId'])
    user_sync(user_info['id'])
