from fastapi import APIRouter,Form
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time
from selenium.webdriver.common.by import By
from helper.emoji import remove_emoji


lazada = APIRouter()

@lazada.post("/lazada/search/") #วางลิ้ง
async def searchlazada(linkproduct: str = Form()):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
    )
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options=chrome_options)
        # driver.get('https://www.shopee.co.th')


    driver.get('{}'.format(linkproduct))
    time.sleep(1)
    try:
        time.sleep(1)
        closepopup=driver.find_element_by_class_name('sfo__close')
        closepopup.click()

    except:
        print("ไม่มีโฆษณาให้ปิด")
    # thai_lang = driver.find_element_by_class_name('shopee-button-outline.shopee-button-outline--primary-reverse')
    # thai_lang.click()


        # flex-auto flex-column  swTqJe
    # maindetail = driver.find_element_by_class_name('flexitems-center.ag8Oq-')

    data_dict_list = []

    # header_dict_list={}
    pricetag=driver.find_element_by_class_name('pdp-price.pdp-price_type_normal.pdp-price_color_orange.pdp-price_size_xl').text
    time.sleep(0.2)
    pricetag=pricetag.replace('฿', '')
    amoutetag="100"
    matches = re.findall(r'\d+', amoutetag)
    amoutetag = int(matches[0]) if len(matches) > 0 else None

    producturl = driver.current_url


    title=driver.find_element_by_class_name('pdp-mod-product-badge-title')
    title=remove_emoji(title.text)
    title=title.replace("\n", "")
    sold=0
    # province=driver.find_elements_by_class_name("dR8kXc")
    # province=province[-1].text
    # province=province.replace("ส่งจาก\n", "")
    province="None"
    # catagory=driver.find_elements_by_class_name('akCPfg')
    # catagory=catagory[1].text
    catagory="None"
    # try:
    # try:
        
    # except:


    framoption=driver.find_elements_by_class_name("pdp-mod-product-info-section.sku-prop-selection")
    print("frame that works")
    print(len(framoption))
    if  len(framoption)==2:
        headers1=framoption[0].find_element_by_class_name('section-title').text
        headers2=framoption[1].find_element_by_class_name('section-title').text
        header_dict_list={"headerchoie1":headers1,"headerchoie2":headers2}
        try:
            btnzone1=framoption[0].find_element_by_class_name('sku-prop-content')
            btn1nameselected=btnzone1.find_element_by_class_name('sku-variable-size-selected')
            btn1nameselected.click()
            btn1name=btnzone1.find_elements_by_class_name('sku-variable-size')
        
        except:
            btnzone1=framoption[0].find_element_by_class_name('sku-prop-content')
            btn1nameselected=btnzone1.find_element_by_class_name('sku-variable-img-wrap-selected')
            btn1nameselected.click()
            btn1name=btnzone1.find_elements_by_class_name('sku-variable-img-wrap')
        
        btnzone2=framoption[1].find_element_by_class_name('sku-prop-content')
        try:
            btn2nameselected=btnzone2.find_element_by_class_name('sku-variable-name-selected')
        except:
            btn2nameselected=btnzone2.find_element_by_class_name('sku-variable-size-selected')
        btn2nameselected.click()
        btn2name=btnzone2.find_elements_by_class_name('sku-variable-name')

        btn1list=[]
        btn2list=[]
        for btn1 in btn1name:
            btn1.click()
            btnname1text=framoption[0].find_element_by_class_name('sku-name').text
            btn1list.append(btnname1text)
        btn2list=[]
        for btn2 in btn2name:
            btn2list.append(btn2.text) 
        print("มี2ตัวเลือก")

        for btn1 in btn1name:
            btn1.click()
            btnname1text=framoption[0].find_element_by_class_name('sku-name').text
            time.sleep(0.2)
            
            for btn2 in btn2name:
                btn2.click()
                time.sleep(0.2)
                btnname2text=framoption[1].find_element_by_class_name('sku-name').text
                data_dict = dict()
                btn1class = btn1.get_attribute("class")
                btn2class = btn2.get_attribute("class")
                if "disabled" in btn1class or "disabled" in btn2class:
                    framamoute = 0
                    price = 0
                else:
                    framamoute=100  
                    price =driver.find_element_by_class_name("pdp-price.pdp-price_type_normal.pdp-price_color_orange.pdp-price_size_xl").text
                    price = price.replace("฿", "").replace(",", "")
                    price = int(price.split(".")[0])
                    


        
                    # data_dict[header_dict_list["headerchoie1"]] = btn1.text
                    # data_dict[header_dict_list["headerchoie2"]] = btn2.text
                data_dict["choice1"] = btnname1text
                data_dict["choice2"] = btnname2text
                data_dict['amoute'] = framamoute
                data_dict['price'] = price
                    
                data_dict_list.append(data_dict)

    elif len(framoption)==1:
        print('1choice')
        headers1=framoption[0].find_element_by_class_name('section-title').text
        header_dict_list={"headerchoie1":headers1,"headerchoie2":None}
        try:
            btnzone1=framoption[0].find_element_by_class_name('sku-prop-content')
            print(btnzone1.text)
        except:
            print('erorr')


        
        
        try:
            try:
                btn1nameselected=btnzone1.find_element_by_class_name('sku-variable-size-selected')
            except:
                btn1nameselected=btnzone1.find_element_by_class_name('sku-variable-name-selected')
                print(btn1nameselected.text)
        except:
            btn1nameselected=btnzone1.find_element_by_class_name('sku-variable-img-wrap-selected')
            
        btn1nameselected.click()



        # framoption=driver.find_elements_by_class_name("pdp-mod-product-info-section.sku-prop-selection")
        # btnzone1=framoption[0].find_element_by_class_name('sku-prop-content')
        
        
        try:
            print('that work btn1')
            btn1name = btnzone1.find_elements_by_class_name('sku-variable-name')
            if len(btn1name) < 1:
                raise Exception("Error: No elements found1.")
            print(framoption[0].text)
        except Exception as e:
            print(str(e))
            try:
                btn1name = btnzone1.find_elements_by_class_name('sku-variable-img-wrap')
                print('that work btn2')
                if len(btn1name) < 1:
                    raise Exception("Error: No elements found2.")
            except Exception as e:
                print(str(e))
                try:
                    btn1name = btnzone1.find_elements_by_class_name('sku-variable-size')
                    print('that work btn3')
                    if len(btn1name) < 1:
                        raise Exception("Error: No elements found3.")
                except Exception as e:
                    print(str(e))


        
                
            
        
                
            
            
        


        btn1list=[]

        # for btn1 in btn1name:
        #     print('clickwork')
        #     btn1.click()
        #     time.sleep(0.2)
        #     btnname1text=framoption[0].find_element_by_class_name('sku-name').text
        #     btn1list.append(btnname1text)


        for btn1 in btn1name:
        
            data_dict = dict()
            btn1.click()
            try:
                btnname1text=framoption[0].find_element_by_class_name('sku-name').text
            except:
                btnname1text=btn1.text
            time.sleep(0.2)
            btn1list.append(btnname1text)
            btn1class = btn1.get_attribute("class")
            if "disabled" in btn1class:
                framamoute = 0
                price = 0
            else:
                framamoute=100  
                price =driver.find_element_by_class_name("pdp-price.pdp-price_type_normal.pdp-price_color_orange.pdp-price_size_xl").text
                price = price.replace("฿", "").replace(",", "")
                price = int(price.split(".")[0])

                data_dict["choice1"] = btnname1text
                data_dict['amoute'] = framamoute
                data_dict['price'] = price
                    
                data_dict_list.append(data_dict)
    else:
        print('ไม่มีตัวเลือก')
        try:
            price =driver.find_element_by_class_name("pdp-price.pdp-price_type_normal.pdp-price_color_orange.pdp-price_size_xl").text
        except:
            price=0
        
                
        


    try:
        outsidecoutry="ภายในประเทศ"
        # outsidecoutry = driver.find_element_by_class_name("flex.items-center.ag8Oq-").text #นานกว่าปกติ

    except:
        outsidecoutry="ภายในประเทศ"
        # blogimg=driver.find_element_by_class_name("XjROLg")
        # print(blogimg.text)
        print()
    img_list=[]
    time.sleep(2)
    imgs=driver.find_elements_by_class_name("pdp-mod-common-image.item-gallery__thumbnail-image")
    time.sleep(1)
    for urlimage in imgs:
        img_dict = dict()
        urlimage=urlimage.get_attribute('src')
        img_dict['image']=urlimage
        img_list.append(img_dict)

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
        # info_dict_list.append(info_dict)0000000000000000000000000000000000000
    if len(framoption)==2:
        alllist=[{"selectnumber":2},{"info":info_dict},{"header":header_dict_list,},{"datalist":data_dict_list},{"images":img_list},{"btnlist1":btn1list},{"btnlist2":btn2list}]
            # alllist=[2,info_dict,header_dict_list,data_dict_list,img_list,btn1list,btn2list]
    elif len(framoption)==1:
        alllist=[{"selectnumber":1},{"info":info_dict},{"header":header_dict_list,},{"datalist":data_dict_list},{"images":img_list},{"btnlist1":btn1list}]
    else:
        alllist=[{"selectnumber":0},{"info":info_dict},{"images":img_list}]
    driver.quit()
    return alllist 

