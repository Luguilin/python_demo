# -*- coding: utf-8 -*-
import random
import time, re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import requests
from io import BytesIO
from tempmail3 import *
from captcha_qq import CaptchaQQ

class Vincent(object):
    def __init__(self):
        
        chrome_option = webdriver.ChromeOptions()

        chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_option.add_argument('--user-agent=Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
        chrome_option.add_argument('--disable-extensions')
        chrome_option.add_argument('--profile-directory=Default')
        chrome_option.add_argument("--incognito")
        chrome_option.add_argument("--disable-plugins-discovery")
        chrome_option.add_argument("--start-maximized")


        # chrome_option.set_headless()

        # self.driver = webdriver.Chrome(executable_path=r"/Users/gary/Downloads/chromedriver", chrome_options=chrome_option)
        # self.driver = webdriver.Chrome(executable_path=r"/Users/gary/Program/Python/processon/chromedriver", chrome_options=chrome_option)
        self.driver = webdriver.Chrome(executable_path=r"./chromedriver", chrome_options=chrome_option)
        # self.driver =webdriver.Chrome("D:\Google\Chrome\Application\chromedriver.exe")
        self.driver.set_window_size(1440, 900)

    def visit_index(self):
        # self.driver.get("https://www.Vincent.com/")
        # 

        # self.driver.get("https://www.processon.com/signup")

        self.driver.get("https://www.processon.com/i/5955c8cfe4b08b003f31733e") # 桂林
        # self.driver.get("https://www.processon.com/i/59f14fabe4b0f07c05f785a2") # 志扬
        
        
        elemt_register = self.driver.find_element_by_css_selector(".button")
        elemt_register.click()#进入都注册页面


        email=make()

        print(email.my_email_address)


        elemt_login_phone = self.driver.find_element_by_id("login_phone")
        elemt_login_phone.send_keys(email.my_email_address)#给标签输入值


        elemt_tencent_btn = self.driver.find_element_by_id("tencent_btn")
        elemt_tencent_btn.click()
        time.sleep(3)

        button_text="获取验证码"
        auto_drop=True

        while button_text=="获取验证码":

            time.sleep(1)

            print("等待拖动验证码")
            # try:
            #     print("等待拖动验证码")
            #     if auto_drop:
            #         _captcha_qq = CaptchaQQ()
            #         _captcha_qq.login_main(self.driver)
            # except:
            #     auto_drop=False
            #     print("自动滑动图片失败")
            
            button_text=elemt_tencent_btn.text
            
            

        print("通过，正在获取验证码")

        email=getCode(email)

        print(email.code)


        elemt_login_verify = self.driver.find_element_by_id("login_verify")
        elemt_login_verify.send_keys(email.code)


        elemt_login_password = self.driver.find_element_by_id("login_password")
        elemt_login_password.send_keys(email.user+"12345")


        elemt_login_fullname = self.driver.find_element_by_id("login_fullname")
        elemt_login_fullname.send_keys(email.user+"12345")
        
        


        elemt_signup_btn = self.driver.find_element_by_id("signup_btn")
        elemt_signup_btn.click()

        time.sleep(3)

        # self.driver.close()
        self.driver.quit()

        return 1

        # 
        # WebDriverWait(self.driver, 10, 0.5).until(
            # EC.element_to_be_clickable((By.XPATH, '//div[@class="gt_slider_knob gt_show"]')))

        # 进入模拟拖动流程
        # self.analog_drag()

    def analog_drag(self):
        # 鼠标移动到拖动按钮，显示出拖动图片
        element = self.driver.find_element_by_xpath('//div[@class="gt_slider_knob gt_show"]')
        ActionChains(self.driver).move_to_element(element).perform()
        time.sleep(3)

        # 刷新一下极验图片
        element = self.driver.find_element_by_xpath('//a[@class="gt_refresh_button"]')
        element.click()
        time.sleep(1)

        # 获取图片地址和位置坐标列表
        cut_image_url, cut_location = self.get_image_url('//div[@class="gt_cut_bg_slice"]')
        full_image_url, full_location = self.get_image_url('//div[@class="gt_cut_fullbg_slice"]')

        # 根据坐标拼接图片
        cut_image = self.mosaic_image(cut_image_url, cut_location)
        full_image = self.mosaic_image(full_image_url, full_location)

        # 保存图片方便查看
        cut_image.save("cut.jpg")
        full_image.save("full.jpg")

        # 根据两个图片计算距离
        distance = self.get_offset_distance(cut_image, full_image)

        # 开始移动
        self.start_move(distance)

        # 如果出现error
        try:
            WebDriverWait(self.driver, 5, 0.5).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="gt_ajax_tip gt_error"]')))
            print("验证失败")
            return
        except TimeoutException as e:
            pass

        # 判断是否验证成功
        s = self.driver.find_elements_by_xpath('//*[@id="wrap1"]/div[3]/div/div/p')
        if len(s) == 0:
            print("滑动解锁失败,继续尝试")
            self.analog_drag()
        else:
            print("滑动解锁成功")
            time.sleep(1)
            ss=self.driver.find_element_by_xpath('//*[@id="wrap1"]/div[3]/div/div/div[2]').get_attribute("onclick")
            print(ss)
            ss=self.driver.find_element_by_xpath('//*[@id="wrap1"]/div[3]/div/div/div[2]').click()



    # 获取图片和位置列表
    def get_image_url(self, xpath):
        link = re.compile('background-image: url\("(.*?)"\); background-position: (.*?)px (.*?)px;')
        elements = self.driver.find_elements_by_xpath(xpath)
        image_url = None
        location = list()
        for element in elements:
            style = element.get_attribute("style")
            groups = link.search(style)
            url = groups[1]
            x_pos = groups[2]
            y_pos = groups[3]
            location.append((int(x_pos), int(y_pos)))
            image_url = url
        return image_url, location

    # 拼接图片
    def mosaic_image(self, image_url, location):
        resq = requests.get(image_url)
        file = BytesIO(resq.content)
        img = Image.open(file)
        image_upper_lst = []
        image_down_lst = []
        for pos in location:
            if pos[1] == 0:
                # y值==0的图片属于上半部分，高度58
                image_upper_lst.append(img.crop((abs(pos[0]), 0, abs(pos[0]) + 10, 58)))
            else:
                # y值==58的图片属于下半部分
                image_down_lst.append(img.crop((abs(pos[0]), 58, abs(pos[0]) + 10, img.height)))

        x_offset = 0
        # 创建一张画布，x_offset主要为新画布使用
        new_img = Image.new("RGB", (260, img.height))
        for img in image_upper_lst:
            new_img.paste(img, (x_offset, 58))
            x_offset += img.width

        x_offset = 0
        for img in image_down_lst:
            new_img.paste(img, (x_offset, 0))
            x_offset += img.width

        return new_img

    # 判断颜色是否相近
    def is_similar_color(self, x_pixel, y_pixel):
        for i, pixel in enumerate(x_pixel):
            if abs(y_pixel[i] - pixel) > 50:
                return False
        return True

    # 计算距离
    def get_offset_distance(self, cut_image, full_image):
        for x in range(cut_image.width):
            for y in range(cut_image.height):
                cpx = cut_image.getpixel((x, y))
                fpx = full_image.getpixel((x, y))
                if not self.is_similar_color(cpx, fpx):
                    img = cut_image.crop((x, y, x + 50, y + 40))
                    # 保存一下计算出来位置图片，看看是不是缺口部分
                    img.save("1.jpg")
                    return x

    # 开始移动
    def start_move(self, distance):
        element = self.driver.find_element_by_xpath('//div[@class="gt_slider_knob gt_show"]')

        # 这里就是根据移动进行调试，计算出来的位置不是百分百正确的，加上一点偏移
        distance -= element.size.get('width') / 2
        distance += 15

        # 按下鼠标左键
        ActionChains(self.driver).click_and_hold(element).perform()
        time.sleep(0.5)
        while distance > 0:
            if distance > 10:
                # 如果距离大于10，就让他移动快一点
                span = random.randint(5, 8)
            else:
                # 快到缺口了，就移动慢一点
                span = random.randint(2, 3)
            ActionChains(self.driver).move_by_offset(span, 0).perform()
            distance -= span
            time.sleep(random.randint(10, 50) / 100)

        ActionChains(self.driver).move_by_offset(distance, 1).perform()
        ActionChains(self.driver).release(on_element=element).perform()

if __name__ == "__main__":
    h = Vincent()
    code=h.visit_index()

    while code==1:
        h = Vincent()
        code=h.visit_index()



