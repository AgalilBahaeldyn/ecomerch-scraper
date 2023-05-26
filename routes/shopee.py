from fastapi import APIRouter,Form
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time
from selenium.webdriver.common.by import By

from helper.emoji import remove_emoji
# from starlette.status import HTTP_204_NO_CONTENT


shopee = APIRouter()

@shopee.post("/shopee/search/") #วางลิ้ง
async def login(linkproduct: str = Form()):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
    # driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options=chrome_options)
        # driver.get('https://www.shopee.co.th')
    
    driver.get('https://shopee.co.th/buyer/login?next=https%3A%2F%2Fshopee.co.th%2F')
    time.sleep(3)
    thai_lang = driver.find_element_by_class_name('shopee-button-outline.shopee-button-outline--primary-reverse')
    thai_lang.click()
    time.sleep(1)
    formtext=driver.find_elements_by_class_name('pDzPRp')
    formtext[0].send_keys("0642257745")
    formtext[1].send_keys("Mtbbg743")
    loginbtn=driver.find_element_by_class_name('wyhvVD')
    time.sleep(1)
    loginbtn.click()
    time.sleep(3)

    driver.get('{}'.format(linkproduct))
    time.sleep(3)
    

        # flex-auto flex-column  swTqJe
    # maindetail = driver.find_element_by_class_name('flexitems-center.ag8Oq-')

    data_dict_list = []

    # header_dict_list={}
    pricetag=driver.find_element_by_class_name('pqTWkA').text
    time.sleep(0.2)
    pricetag=pricetag.replace('฿', '')
    amoutetag=driver.find_element_by_class_name("flex.items-center._6lioXX").text
    matches = re.findall(r'\d+', amoutetag)
    amoutetag = int(matches[0]) if len(matches) > 0 else None

    producturl = driver.current_url


    title=driver.find_element_by_class_name('_44qnta')
    title=remove_emoji(title.text)
    title=title.replace("\n", "")
    sold=driver.find_element_by_class_name("P3CdcB").text
    province=driver.find_elements_by_class_name("dR8kXc")
    province=province[-1].text
    province=province.replace("ส่งจาก\n", "")
    catagory=driver.find_elements_by_class_name('akCPfg')
    catagory=catagory[1].text
    try:
    
        framoption=driver.find_element_by_class_name("flex.rY0UiC.j9be9C")
        framesuboption=framoption.find_elements_by_class_name("flex.items-center.bR6mEk") 
        
        
    
        if len(framesuboption)==2:
            headers=framoption.find_elements_by_class_name('oN9nMU')
            header_dict_list={"headerchoie1":headers[0].text,"headerchoie2":headers[1].text}
            btn1name=framesuboption[0].find_elements_by_class_name('product-variation')
            btn1list=[]
            btn2list=[]
            for btn1 in btn1name:
                btn1list.append(btn1.text)
            
            btn2name=framesuboption[1].find_elements_by_class_name('product-variation')
            btn2list=[]
            for btn2 in btn2name:
                btn2list.append(btn2.text)
              
            print("มี2ตัวเลือก")
            btnchoie1=framesuboption[0].find_elements_by_class_name('product-variation')
            btnchoie2=framesuboption[1].find_elements_by_class_name('product-variation')
            # เก็บข้อมูลอาเรย
            # arrbtn1=[]
            # arrbtn2=[]
            # arramouute=[]
            # arrprice=[]

            for btn1 in btnchoie1:
                btn1.click()
                # time.sleep(0.1)
                # print(btn1.text)
                for btn2 in btnchoie2:
                    btn2.click()
                    time.sleep(0.1)
                    # print(btn1.text)
                    # print(btn2.text)
                    data_dict = dict()
                    btn1class = btn1.get_attribute("class")
                    btn2class = btn2.get_attribute("class")
                    if "disabled" in btn1class or "disabled" in btn2class:

                        framamoute = 0
                        # print(framamoute)
                        price = 0
                        # print(price)

                    else:
                        framamoute=driver.find_element_by_class_name("flex.items-center._6lioXX").text #จำนวน
                        time.sleep(0.1)
                        # framamoute = framamoute.replace("จำนวน", "")
                        # framamoute = framamoute.replace("มีสินค้าทั้งหมด", "")
                       
                        matches = re.findall(r'\d+', framamoute)
                        framamoute = int(matches[0]) if len(matches) > 0 else None
                       
                       
                        price =driver.find_element_by_class_name("pqTWkA").text
                        # matches = re.findall(r'\d+', price)
                        # price = int(matches[0]) if len(matches) > 0 else None
                        price = int(price.replace("฿", "").replace(",", ""))
                       

        
                    # data_dict[header_dict_list["headerchoie1"]] = btn1.text
                    # data_dict[header_dict_list["headerchoie2"]] = btn2.text
                    data_dict["choice1"] = btn1.text
                    data_dict["choice2"] = btn2.text
                    data_dict['amoute'] = framamoute
                    data_dict['price'] = price
                    
                    data_dict_list.append(data_dict)

            
        elif len(framesuboption)==1:
            headers=framoption.find_elements_by_class_name('oN9nMU')
            header_dict_list={"headerchoie1":headers[0].text}
            btn1name=framesuboption[0].find_elements_by_class_name('product-variation')
            btn1list=[]
            btn2list=[]
            for btn1 in btn1name:
                btn1list.append(btn1.text)
            print("มี1ตัวเลือก")
            btnchoie=framesuboption[0].find_elements_by_class_name('product-variation')
            for btn in btnchoie:
                btn.click()
                time.sleep(0.1)
                data_dict = dict()
                btnclass = btn.get_attribute("class")
                if "disabled" in btnclass:
                    framamoute = 0
                    price = 0
                else:
                    framamoute=driver.find_element_by_class_name("flex.items-center._6lioXX").text #จำนวน
                    time.sleep(0.1)
                    # framamoute = framamoute.replace("จำนวน", "")
                    # framamoute = framamoute.replace("มีสินค้าทั้งหมด", "")
                    matches = re.findall(r'\d+', framamoute)
                    framamoute = int(matches[0]) if len(matches) > 0 else None

                    
                    price =driver.find_element_by_class_name("pqTWkA").text
                    # matches = re.findall(r'\d+', price)
                    # price = int(matches[0]) if len(matches) > 0 else None
                    price = int(price.replace("฿", "").replace(",", ""))

                data_dict["choice1"] = btn.text
                data_dict['amoute'] = framamoute
                data_dict['price'] = price
                data_dict_list.append(data_dict)
        else:
            print('ไม่มีตัวเลือก')
            price =driver.find_element_by_class_name("pqTWkA").text
            price
    except:
        print()

    try:
        outsidecoutry="ภายในประเทศ"
        outsidecoutry = driver.find_element_by_class_name("flex.items-center.ag8Oq-").text #นานกว่าปกติ

    except:
    
        # blogimg=driver.find_element_by_class_name("XjROLg")
        # print(blogimg.text)
        print()
    img_list=[]
    time.sleep(2)
    imgs=driver.find_elements_by_class_name("A4dsoy")
    time.sleep(1)
    for urlimage in imgs:
            
        urlimage=urlimage.get_attribute('style')
        img_dict = dict()
        match = re.search(r'background-image:\s*url\((.*?)\)', urlimage)
        if match:
            background_image_url = match.group(1)
            background_image_url=background_image_url[1:-1]
            img_dict['image'] = background_image_url
            img_list.append(img_dict)
            # print(background_image_url)
        else:
            print('No background image found')
    # info_dict_list=[]
    info_dict=dict()
    info_dict['producturl']=producturl
    info_dict['catagory'] = catagory
    info_dict['title'] = title
    info_dict['sold'] = sold
    info_dict['amoutetag'] = amoutetag
    info_dict['pricetag'] = pricetag
    info_dict['province'] =province
    info_dict['abroad']=outsidecoutry
    # info_dict_list.append(info_dict)
    if len(framesuboption)==2:
        alllist=[{"selectnumber":2},{"info":info_dict},{"header":header_dict_list,},{"datalist":data_dict_list},{"images":img_list},{"btnlist1":btn1list},{"btnlist2":btn2list}]
        # alllist=[2,info_dict,header_dict_list,data_dict_list,img_list,btn1list,btn2list]
    elif len(framesuboption)==1:
        alllist=[{"selectnumber":1},{"info":info_dict},{"header":header_dict_list,},{"datalist":data_dict_list},{"images":img_list},{"btnlist1":btn1list}]
    else:
        alllist=[{"selectnumber":0},{"info":info_dict},{"images":img_list}]

    # print(alllist)
    driver.quit()
    return alllist


# @shopee.post("/shopee/search/") #วางลิ้ง
# async def login(linkproduct: str = Form()):

@shopee.post("/shopee/flashsale")
def get_flashsale():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
    # driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options=chrome_options)
        # driver.get('https://www.shopee.co.th')
    
    driver.get('https://shopee.co.th/')
    thai_lang = driver.find_element_by_class_name('shopee-button-outline.shopee-button-outline--primary-reverse')
    thai_lang.click()
    close_popup = driver.execute_script("return document.querySelector('shopee-banner-popup-stateful').shadowRoot.querySelector('div.shopee-popup__close-btn')")
    close_popup.click()
    # driver.execute_script("document.body.style.zoom='10%'")

    flashsalebox=driver.find_element_by_class_name('PF1fuW')
    time.sleep(2)
    nextbtn=flashsalebox.find_element_by_class_name('carousel-arrow.carousel-arrow--next.carousel-arrow--hint')
    svgicon=nextbtn.find_element_by_tag_name('svg')
    # svgicon.click()
    # time.sleep(1)
    # svgicon.click()
    time.sleep(2)

    data_dict_list=[]
    col=flashsalebox.find_elements_by_class_name('image-carousel__item')
    for product in col:
        time.sleep(1)
        data_dict = dict()
        price = product.find_element_by_class_name('hSM8kk').text
        price=price.replace('฿\n',"")
        sold=product.find_element_by_class_name('eNmE7o.RJ6Vpu').text
        try:
            image=product.find_element_by_class_name('wP9-V9.WPIj4t')
        except:
            svgicon.click()
            time.sleep(2)
            image=product.find_element_by_class_name('wP9-V9.WPIj4t')
        
        urlimage=image.get_attribute('style')
        match = re.search(r'background-image:\s*url\((.*?)\)', urlimage)
        if match:
            background_image_url = match.group(1)
            background_image_url=background_image_url[1:-1]
            image = background_image_url

        data_dict['price'] = price
        data_dict['images'] = image
        data_dict['sold'] = sold
        data_dict_list.append(data_dict)
    driver.quit()
    return data_dict_list


@shopee.post("/shopee/diary")
def get_diary():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
    
    driver.get('https://shopee.co.th/')
    thai_lang = driver.find_element_by_class_name('shopee-button-outline.shopee-button-outline--primary-reverse')
    thai_lang.click()
    close_popup = driver.execute_script("return document.querySelector('shopee-banner-popup-stateful').shadowRoot.querySelector('div.shopee-popup__close-btn')")
    close_popup.click()
    driver.execute_script("document.body.style.zoom='10%'")
    time.sleep(2)

    diarybox=driver.find_element_by_class_name('stardust-tabs-panels')
    time.sleep(1.5)
    data_dict_list=[]
    col=diarybox.find_elements_by_class_name('nH7cMF')
    for product in col:
        time.sleep(0.5)
        data_dict = dict()
        price = product.find_element_by_class_name('_3KqMTq').text
        title=product.find_element_by_class_name('sUq1Dr._1M8qaS')
        title=remove_emoji(title.text)
        sold=product.find_element_by_class_name('_6ykn6M.aO8bXP').text
        image=product.find_element_by_tag_name('img')
        image=image.get_attribute("src")

        data_dict['price'] = price
        data_dict['images'] = image
        data_dict['sold'] = sold
        data_dict['title'] = title
        
        data_dict_list.append(data_dict)
    driver.quit()
    return data_dict_list
