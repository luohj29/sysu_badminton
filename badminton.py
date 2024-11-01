# -*- coding: gbk -*-
import os
import time
from selenium import webdriver
from PIL import Image,ImageFilter
import cv2
from aip import AipOcr
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.common.by import By

# from modelscope.pipelines import pipeline
# from modelscope.utils.constant import Tasks
# import gradio as gr
# import os

# class xiaolv_ocr_model():

#     def __init__(self):
#         model_small = r"./output_small"
#         model_big = r"./output_big"
#         self.ocr_recognition_small = pipeline(Tasks.ocr_recognition, model=model_small)
#         self.ocr_recognition1_big = pipeline(Tasks.ocr_recognition, model=model_big)


#     def run(self,pict_path,moshi = "small", context=[]):
#         pict_path = pict_path.name
#         context = [pict_path]

#         if moshi == "small":
#             result = self.ocr_recognition_small(pict_path)
#         else:
#             result = self.ocr_recognition1_big(pict_path)

#         context += [str(result['text'][0])]
#         responses = [(u, b) for u, b in zip(context[::2], context[1::2])]
#         print(f"识别的结果为：{result}")
#         os.remove(pict_path)
#         return responses,context
    
service = Service('geckodriver/geckodriver.exe') 
netid = 'luohj29'
password = 'RogersLuo6214'
bookdate = '2024-11-01'
playtime = '08:00-09:00'
dir = "/Users/rogers/Documents/learning in cs/CV/badminton/"

width = 280
height = 130
type = 'png'


repadd = dir+"rep.png"
greyadd = dir+"grey.png"
edadd = dir+"edge.png"
resadd =dir+"resize.png"

config = {
    'appId': '116074761',
    'apiKey': 'kzM8AkgUZr41bd2CETiBC64x',
    'secretKey': 'z6duAAgWqDMzpg2vARV0NyJGt3KIaMhQ'
}

client = AipOcr(**config)


driver = webdriver.Firefox()
driver.get("https://gym.sysu.edu.cn/product/show.html?id=35")
driver.maximize_window()
try:
    login_link = driver.find_element(By.XPATH, '//a[text()="登录"]').click()
    # print(login_link.get_attribute('href'))  # 输出 href 属性
except Exception as e:
    print(f"未找到登录链接: {e}")
    driver.quit()

screenshotadd = "/Users/rogers/Documents/learning in cs/CV/badminton/imgscreenshot.png"
codeadd = "/Users/rogers/Documents/learning in cs/CV/badminton/code.png"
rebadd = "/Users/mengjiexu/Documents/badminton/rgb.png"

def ResizeImage(filein, fileout, width, height, img_format):
    img = Image.open(filein)
    out = img.resize((width, height), Image.LANCZOS)  # 使用高质量的重采样
    out.save(fileout, img_format)  # 根据格式保存图像


def clearimage(originadd):
    img = Image.open(originadd)#读取系统的内照片
    #将黑色干扰线替换为白色
    width = img.size[0]#长度
    height = img.size[1]#宽度
    for i in range(0,width):#遍历所有长度的点
        for j in range(0,height):#遍历所有宽度的点
            data = (img.getpixel((i,j)))#打印该图片的所有点
            if (data[0]<=25 and data[1]<=25 and data[2]<=25):#RGBA的r,g,b均小于25
                img.putpixel((i,j),(255,255,255,255))#则这些像素点的颜色改成白色
    img = img.convert("RGB")#把图片强制转成RGB
    img.save(repadd)#保存修改像素点后的图片
    #灰度化
    Grayimg = cv2.cvtColor(cv2.imread(repadd), cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(Grayimg, 160, 255,cv2.THRESH_BINARY)
    cv2.imwrite(greyadd, thresh)
    #提取边缘
    edimg = Image.open(greyadd)
    conF = edimg.filter(ImageFilter.CONTOUR)
    conF.save(edadd)

def img_to_str(image_path):
    identicode = ""
    image = open(image_path,'rb').read()
    result = client.basicGeneral(image)
    
    with open("/Users/rogers/Documents/learning in cs/CV/badminton/result.txt","a") as f:
        for line in result["words_result"]:
            identicode =identicode+line["words"]
            f.write(line["words"]+"\n")
    return(identicode)

def getidentify(originadd):
    clearimage(originadd)
    ResizeImage(edadd, resadd, width, height, type)
    identicode = img_to_str(resadd)
    return(identicode)


def Convertimg():
    imglocation = ("//img[@name='captchaImg']")
    driver.save_screenshot(screenshotadd)
    im = Image.open(screenshotadd)
    left = driver.find_element(By.XPATH, imglocation).location['x']
    top = driver.find_element(By.XPATH, imglocation).location['y']
    right = driver.find_element(By.XPATH, imglocation).location['x'] + driver.find_element(By.XPATH, imglocation).size['width']
    bottom = driver.find_element(By.XPATH, imglocation).location['y'] + driver.find_element(By.XPATH, imglocation).size['height']
    im = im.crop((left, top, right, bottom))
    im.save(codeadd)


def Login():
    driver.find_element(By.XPATH, "//input[@id='username']").send_keys(netid)
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password)
    Convertimg()
    txtcode = getidentify(codeadd)
    print('验证码', txtcode)
    driver.find_element(By.XPATH, "//input[@id='captcha']").send_keys(txtcode)
    time.sleep(2)
    driver.find_element(By.XPATH, "//input[@type='submit']").click()

def bookfield(bookdate,playtime):
    driver.get("https://gym.sysu.edu.cn/product/show.html?id=35")
    # get current time
    import time
    t = time.localtime()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
    # print(current_time)
    #get the hour of the current time
    current_hour = int(time.strftime("%H", t))
    print(current_hour)
    if (current_hour >= 22 and current_hour < 24):
        print("当前时间大于1点,无法订场")
        driver.find_element(By.NAME, "确认").click()
    else:
        print("当前时间可以订场,正在火热抢场ing!!!")
    
    # driver.find_element(By.XPATH, "//a[@href='/product/index.html']").click()
    # driver.find_element(By.XPATH, "//input[@id='txt_name']").send_keys('英东羽毛球场')
    # driver.find_element(By.XPATH, "//button[@type='submit']").click()
    driver.find_element(By.XPATH, '//a[text()="预订"]').click()
    # driver.execute_script("arguments[0].click();", target)
    time.sleep(2)
    driver.find_element(By.XPATH, "//li[@data='%s']"%bookdate).click() #找到对应日期的场地
    if int(playtime[:2])<15:
        js = "window.scrollTo(0,500)"
    else:
        js = "window.scrollTo(0,950)"
    driver.execute_script(js)
    candidates = driver.find_elements(By.XPATH, "//span[@data-timer='%s']"%playtime)
    for can in candidates:
        isbooked = can.get_attribute('class')
        if isbooked == "cell badminton easyui-tooltip":  #找到可用的场地
            print("找到可用场地")
            can.click()
            driver.execute_script("window.scrollTo(0,500)")
            driver.find_element(By.XPATH, "//button[@id='reserve']").click()
            time.sleep(2)
            driver.find_element(By.XPATH, "//button[@id='reserve']").click()
            break
        else:
            pass


var=0
while var >= 0:
    driver.find_element(By.ID, 'username').clear() #清空输入框
    driver.find_element(By.ID, 'password').clear()  #清空输入框
    driver.find_element(By.ID, 'captcha').clear()
    Login()
    var = var+1
    print("这是第%d次登录尝试"%var)
    time.sleep(3)
    try:
        driver.find_element(By.XPATH, "//strong[contains(text(),'罗弘杰')]")
        print("第%d次登录尝试成功，开始订场"%var)
        falg = bookfield(bookdate, playtime)
        if falg==0:
            print("时间未到，无法订场")
            exit()
        print("订场完成")
        print("订场日期为：%s"%bookdate)
        print("订场时段为：%s"%playtime)
        break
    except:
        print("第%d次登录尝试失败，重新尝试"%var)