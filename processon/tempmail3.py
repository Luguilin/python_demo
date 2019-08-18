import requests
from pyquery import PyQuery as pq
import re
import random
import time



class eMail:
    my_email_address=""
    user=""
    domain=""
    sender=""
    title=""
    href=""
    _mail_id=""
    code=""


    def get_id(self):
        if self._mail_id=="":
            self._mail_id=self.href.lstrip('https://temp-mail.org/zh/view/')
        return self._mail_id



def mail(email):

    ss_mail = requests.Session()
    rsp_get = ss_mail.get("https://temp-mail.org/zh/option/change/")
    csrf = re.findall(r'name="csrf" value="(\w+)', rsp_get.text)[0]

    tempmail = {"csrf": csrf, "mail": email.user, "domain": email.domain}

    ss_mail.post("https://temp-mail.org/zh/option/change/", data=tempmail)

    # rsp_refresh = ss_mail.get("https://temp-mail.org/zh/option/refresh/")
    # url_box = re.findall(r"https://temp-mail.org/zh/view/\w+", rsp_refresh.text)

    # mail_box={}
    while True:
        time.sleep(3)
        rsp_refresh = ss_mail.get("https://temp-mail.org/zh/option/refresh/")

        url_box=pq(rsp_refresh.text)(".inbox-dataList")("ul")("li")

        ss_mail.close()

        if url_box!=[]:
            box=pq(url_box[0])
            # email=eMail()
            email.sender=box(".inboxSenderEmail")
            email.title=box(".title-subject")
            email.href=box(".m-link-view")("a").attr("href")
            return email


        # for box in url_box:
        # 	box=pq(box)
        # 	email=eMail()
        # 	email.sender=box(".inboxSenderEmail")
        # 	email.title=box(".title-subject")
        # 	email.href=box(".m-link-view")("a").attr("href")
        #     return email
        	# key=email.get_id()

        	# if key not in mail_box:
        	# 	mail_box[key]=email
        	# else:
        	# 	pass

    # return mail_box

def get_domain():
    r = requests.get("https://temp-mail.org/en/option/change/")
    doc = pq(r.text)
    domains=doc("#domain")("option")
    domain=pq(random.choice(domains)).text()
    return domain



def getuser():
    user = str(random.randint(1000000, 9999999))
    return user


def make():

    email=eMail()
    email.user=getuser()
    email.domain=get_domain()

    email.my_email_address=email.user+email.domain

    return email

	# return mail(user, domain)


def getCode(email):

    email=mail(email)
    r = requests.get(email.href)
    doc = pq(r.text)
    code_str=doc(".inbox-data-content-intro")("strong").text()
    email.code=code_str
    return email


# if __name__ == "__main__":
    # url = "https://www.processon.com/i/5955c8cfe4b08b003f31733e"
    # make()
    # code_str=getCode()
    # print(code_str)




    # 



# https://temp-mail.org/zh/view/c70b4dcbc429b2364dde1dafb5a12b61
