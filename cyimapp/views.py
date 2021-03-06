from django.shortcuts import render
from linebot.models.actions import PostbackAction, URIAction
from linebot.models.events import PostbackEvent
from linebot.models.flex_message import FlexContainer
from linebot.models.send_messages import ImageSendMessage
from cyimapp.models import foodTable,UbikeData
from django.conf import settings
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage,TemplateSendMessage,CarouselTemplate,QuickReply, messages,FlexSendMessage
from linebot.models import QuickReplyButton,MessageAction,LocationAction
from urllib import parse#中文URL轉碼
from urllib.parse import parse_qsl
from templates import replyCarousel

from cyimapp.myLibrary.distance import haversine #計算距離
from cyimapp.myLibrary.real_ubike import getUbikeInfo,loadData #取得Ubike資訊
from datetime import datetime, time
import time
from random import sample
import requests
import json

# Create your views here.
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

#domain = 'https://7c4efa7437bd.ngrok.io'+'/' #本地端網域       #### 測試時請使用這個(註解下方的domain)####
domain = 'https://res.cloudinary.com/lwyuki/image/upload/v1'+'/'#### cloudinary網域(上傳github請使用這個) ####


# 食物區快速回覆
def food_quick_reply():
    message=TextSendMessage(
        text="請選擇功能",
        quick_reply=QuickReply(
        items=[
            QuickReplyButton(action=MessageAction(label="時段推薦",text="/時段推薦")),#回傳文字
            QuickReplyButton(action=LocationAction(label="定位搜尋")),#傳回定位資訊
            QuickReplyButton(action=URIAction(label="菜單搜尋",uri='https://liff.line.me/1655990146-4dZdvw9P',
             alt_uri='https://liff.line.me/1655990146-4dZdvw9P')),#網頁連結
            ]
        )
    )
    return message


###飲食區功能###
def foodArea(event):
    if event.message.type=='text':
        
        #如果收到/飲食區，傳快速回覆訊息
        if event.message.text=='/飲食區':
            line_bot_api.reply_message(event.reply_token,food_quick_reply() )


        #隨機推薦此時段的店家
        elif event.message.text=="/時段推薦" :
            food_entry_list = list(foodTable.objects.all()) #取出所有food資料
            myTime = datetime.now().time()
            columns = []
            foodOpenId = []
            for food_item in food_entry_list:
                if food_item.fStartTime!=None and food_item.fEndTime!=None:
                    if food_item.fStartTime <= myTime and food_item.fEndTime >= myTime:
                        foodOpenId.append(food_item.id)  # 將此時段營業的店家id記錄下來
                        
            #如果有5家以上的店營業，隨機挑5筆
            if len(foodOpenId)>=5:
                foodOpenId = sample(foodOpenId,5)
            elif len(foodOpenId)==0:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "目前資料無營業中店家..."))
                return None

            for foodid in foodOpenId:
                unit = foodTable.objects.filter( id = foodid ) # 找出有營業店家的資料
                for item in unit:
                    addCarouselItem(item,columns)
            
            message =  {
                "type": "carousel",
                "contents": columns
            }
            message = FlexSendMessage(alt_text="test",contents=message)
            #傳回5筆以內有在營業的店家
            line_bot_api.reply_message(event.reply_token,message )

    elif event.message.type=='location':  #距離推薦
        food_entry_list = list(foodTable.objects.all()) #取出所有food資料
        #計算自己與所有店家的距離
        foodsDistance = dict() #建立字典("店家":與自己的距離)
        
        for food_item in food_entry_list:
            #計算距離
            if food_item.fLongitude != "" and food_item.fLatitude != "":
                dist = haversine( event.message.longitude, event.message.latitude, float(food_item.fLongitude) , float(food_item.fLatitude) )
                foodsDistance.update({food_item.id:dist})
        sortedFoods = sorted(foodsDistance.items(), key=lambda d: d[1])[:5] #按照值做排序

        columns=[]
        for foodDict in sortedFoods:
            unit = foodTable.objects.filter( id = foodDict[0] ) #過濾資料
            for item in unit:
                addCarouselItem(item,columns)
        
        message =  {
            "type": "carousel",
            "contents": columns
        }
        message = FlexSendMessage(alt_text="test",contents=message)
        #print(message)
        #傳回5個最近的店家
        line_bot_api.reply_message(event.reply_token,message)
    return None



# show 資料表
def listfoodTable(request):
    allfoods = foodTable.objects.all().order_by('id')
    return render(request, "listfoodTable.html", locals())


#菜單搜尋
def searchMenu(request):
    allfoods  = foodTable.objects.all().order_by('id')
    if 'fTag' in request.GET:
        allfoods = foodTable.objects.filter( fTag = request.GET['fTag'] )
        return render(request, "searchMenu.html", locals())
    else:
        allfoods = foodTable.objects.all().order_by('id')

    if 'fName' in request.GET:
        f_menu = foodTable.objects.filter( fName = request.GET['fName'] )
        return render(request, "searchMenu.html", locals())
    else:
        allfoods = foodTable.objects.all().order_by('id')
        return render(request, "searchMenu.html", locals())


# 隨機選店家
def randomFood(event):
    #從用戶傳的文字中擷取ftag關鍵字
    columns=[]
    filter_text = " "
    food_entry_list = list(foodTable.objects.all())  #先列出所有食物物件
    #從物件中一一取出fTag來比對使用者的文字
    for food_item in food_entry_list:  
        if food_item.fTag in event.message.text:
            #print(event.message.text +" find "+ food_item.fTag)
            filter_text = food_item.fTag
    unit = foodTable.objects.filter( fTag = filter_text ) #過濾資料
    
    if unit.exists():
        print(unit)
        for item in unit :
            addCarouselItem(item,columns)
        #如果有5筆以上資料，隨機挑5筆
        if len(columns)>=5:
            columns = sample(columns,5)

        return columns
    else:
        return False


# 輸入 要製作成 Carousel的物件，輸出Carousel物件集合 (最多5個)
def addCarouselItem(item,columns):
    url = domain+parse.quote(str(item.fMenuImage).encode('utf-8'))
    print(url)
    message = replyCarousel.FlexReply(item.fUrl,url,item.fName,item.fAddress )
    columns.append(message.contents)
    return None

###上方為飲食區功能###


###交通區功能###
def trafficArea(event):
    if event.message.type=='text':    
        #如果收到/交通區，傳快速回覆訊息
        if event.message.text=='/交通區':
            line_bot_api.reply_message(event.reply_token,traffic_quick_reply() )

    return None


def insertUbike(request):  #第一次新增資料
    with open("a1b4714b-3b75-4ff8-a8f2-cc377e4eaa0f.json","r",encoding="utf-8") as input_file:
        data = json.load(input_file)
        data = data["result"]['records']
    url = "https://data.tycg.gov.tw/api/v1/rest/datastore/a1b4714b-3b75-4ff8-a8f2-cc377e4eaa0f?format=json"
    #data = requests.get(url).json()
    for item in data:
        sno = item["sno"]    #代號
        sna = item["sna"]    #場站名稱
        sbi = item["sbi"]    #可租借數
        bemp = item["bemp"]  #空位數
        unit = UbikeData.objects.create(sno=sno, sna=sna, sbi=sbi, bemp=bemp) 
        unit.save()  #寫入資料庫
    D_bike = UbikeData.objects.all().order_by('id')  #讀取資料表, 依 id 遞減排序
    return render(request, "listUbike.html", locals())

def modifyUbike(request):  #修改資料
    #with open("a1b4714b-3b75-4ff8-a8f2-cc377e4eaa0f.json","r",encoding="utf-8") as input_file:
    #    data = json.load(input_file)
    #    data = data["result"]['records']
    try:
        url = "https://data.tycg.gov.tw/api/v1/rest/datastore/a1b4714b-3b75-4ff8-a8f2-cc377e4eaa0f?format=json"
        data = requests.get(url).json()
        data = data["result"]['records']
    except:
        data = None
    if data:
        for item in data:
            unit = UbikeData.objects.get(sno=item["sno"])
            unit.sbi = item["sbi"]    #可租借數
            unit.bemp = item["bemp"]  #空位數
            unit.save()  #寫入資料庫
        D_bike = UbikeData.objects.all().order_by('id')  #讀取資料表, 依 id 排序
        return render(request, "listUbike.html", locals())
    else:
        ubikeInfo  = UbikeData.objects.all().order_by('id')
        return render(request, "searchUbike.html", locals())

# 交通區快速回覆
def traffic_quick_reply():
    message=TextSendMessage(
        text="請選擇功能",
        quick_reply=QuickReply(
        items=[
            QuickReplyButton(action=PostbackAction(label="公車資訊",data="busInfo=True")),
            QuickReplyButton(action=URIAction(label="Ubike資訊",uri='https://liff.line.me/1655990146-0DxGKVrq',
             alt_uri='https://liff.line.me/1655990146-0DxGKVrq')),#網頁連結
            QuickReplyButton(action=PostbackAction(label="校園地圖",data="campusMap=True"))
            ]
        )
    )
    return message

# 公車資訊快速回覆
def traffic_bus_quick_reply():
    message=TextSendMessage(
        text="請選擇功能",
        quick_reply=QuickReply(
        items=[
	        QuickReplyButton(action=PostbackAction(label="時刻表",data="busTimetable=True")),#Postback事件
            QuickReplyButton(action=URIAction(label="即時規劃",uri='https://liff.line.me/1655990146-mDVw6LaB',
            alt_uri='https://liff.line.me/1655990146-mDVw6LaB')),#連結「桃園公車動態資訊系統」的LIFF

            ]
        )
    )
    return message


#傳送時刻表
def sendBack_bustimetable(event): #Postback
    try:
        message = ImageSendMessage(
            original_content_url='https://res.cloudinary.com/lwyuki/image/upload/v1622563796/static/img/bus/busTimetable_page-0001_ufxph0.jpg', 
            preview_image_url='https://res.cloudinary.com/lwyuki/image/upload/v1622563796/static/img/bus/busTimetable_page-0001_ufxph0.jpg')
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message (event.reply_token, TextSendMessage(text='發生錯誤!'))

#Ubike 資訊
def searchUbike(request):
    ubikeInfo  = UbikeData.objects.all().order_by('id')
    return render(request, "searchUbike.html", locals())
    """
    if 'reload' in request.GET:
        loadData()
        ubikeInfo = getUbikeInfo()
        return render(request, "searchUbike.html", locals())
    else:
        ubikeInfo = getUbikeInfo()
        return render(request, "searchUbike.html", locals())
    """



#使用說明快速回覆
def illustration_quick_reply():
    message=TextSendMessage(
        text="請選擇功能",
        quick_reply=QuickReply(
        items=[
	        QuickReplyButton(action=PostbackAction(label="食物區",data="illuFood=True")),
            QuickReplyButton(action=PostbackAction(label="交通區",data="illuTraffic=True")),
        ]
        )
    )
    return message

#使用說明快速回覆-交通區
def illuTraffic_quick_reply():
    message=TextSendMessage(
        text="請選擇功能",
        quick_reply=QuickReply(
        items=[
	        QuickReplyButton(action=PostbackAction(label="公車資訊",data="illuBus=True")),
            QuickReplyButton(action=PostbackAction(label="Ubike資訊",data="illuUbike=True")),
            QuickReplyButton(action=PostbackAction(label="校園地圖",data="illuCamp=True")),
        ]
        )
    )
    return message


#使用說明快速回覆-食物區
def illuFood_quick_reply():
    message=TextSendMessage(
        text="請選擇功能",
        quick_reply=QuickReply(
        items=[
	        QuickReplyButton(action=PostbackAction(label="時段推薦",data="illuTime=True")),
            QuickReplyButton(action=PostbackAction(label="定位搜尋",data="illuPosi=True")),
            QuickReplyButton(action=PostbackAction(label="菜單搜尋",data="illuMenu=True")),
        ]
        )
    )
    return message


#傳送校園地圖
def sendBack_map(event, backdata): #Postback
    try:
        message = ImageSendMessage(
            original_content_url='https://alumni.cycu.edu.tw/alumni/upload/editor/pic/%E6%A0%A1%E5%8D%80%E5%B9%B3%E9%9D%A2%E5%9C%96.jpg', 
            preview_image_url='https://alumni.cycu.edu.tw/alumni/upload/editor/pic/%E6%A0%A1%E5%8D%80%E5%B9%B3%E9%9D%A2%E5%9C%96.jpg')
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message (event.reply_token, TextSendMessage(text='發生錯誤!'))


###上方為交通區功能###


foodAreaList =['/飲食區','/時段推薦','/菜單搜尋'] #飲食區功能列表
trafficAreaList =['/交通區'] #交通區功能列表


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        
        for event in events:
            if isinstance(event, MessageEvent):
                #文字訊息
                if event.message.type=='text':
                    #飲食區功能
                    if event.message.text in foodAreaList :
                        foodArea(event)
                    #交通區功能
                    elif event.message.text in trafficAreaList :
                        trafficArea(event)
                    elif event.message.text == '/使用說明' :
                        line_bot_api.reply_message(event.reply_token,illustration_quick_reply() )
                    #如果收到/foodTable，傳資料表(測試用)
                    elif event.message.text=="/foodTable" :
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(
                            text='https://liff.line.me/'+'1655990146-npeZ9k20') )
                    #如果收到分類的關鍵字，隨機傳店家資訊(測試用)
                    elif randomFood(event):
                        column=randomFood(event)
                        message =  {
                            "type": "carousel",
                            "contents": column
                        }
                        message = FlexSendMessage(alt_text="test",contents=message)
                        line_bot_api.reply_message(event.reply_token, message)
                    #鸚鵡回話
                    else:
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = event.message.text) )

                #定位訊息
                elif event.message.type=='location':
                    #進入飲食區功能
                    foodArea(event)
                    
            if isinstance(event, PostbackEvent):  #PostbackTemplateAction觸發此事件
                backdata = dict(parse_qsl(event.postback.data))  #取得Postback資料
                if backdata.get('campusMap') == 'True':
                    sendBack_map(event,backdata)
                if backdata.get('busTimetable') == 'True':
                    sendBack_bustimetable(event)
                if backdata.get('busInfo') == 'True':
                    line_bot_api.reply_message(event.reply_token,traffic_bus_quick_reply() )
                if backdata.get('illuFood') == 'True':
                    line_bot_api.reply_message(event.reply_token,illuFood_quick_reply() )
                if backdata.get('illuTraffic') == 'True':
                    line_bot_api.reply_message(event.reply_token,illuTraffic_quick_reply() )
                if backdata.get('illuTime') == 'True':
                    try:
                        message = ImageSendMessage(
                            original_content_url='https://res.cloudinary.com/lwyuki/image/upload/v1623558988/static/img/illustration/%E6%99%82%E6%AE%B5%E6%8E%A8%E8%96%A6_qm3a52.png', 
                            preview_image_url='https://res.cloudinary.com/lwyuki/image/upload/v1623558988/static/img/illustration/%E6%99%82%E6%AE%B5%E6%8E%A8%E8%96%A6_qm3a52.png')
                        line_bot_api.reply_message(event.reply_token, message)
                    except:
                        line_bot_api.reply_message (event.reply_token, TextSendMessage(text='發生錯誤!'))
                if backdata.get('illuPosi') == 'True':
                    try:
                        message = []
                        message.append(ImageSendMessage(
                            original_content_url='https://res.cloudinary.com/lwyuki/image/upload/v1623558987/static/img/illustration/%E5%AE%9A%E4%BD%8D%E6%90%9C%E5%B0%8B1_uvgvsl.png', 
                            preview_image_url='https://res.cloudinary.com/lwyuki/image/upload/v1623558987/static/img/illustration/%E5%AE%9A%E4%BD%8D%E6%90%9C%E5%B0%8B1_uvgvsl.png'))
                        message.append(ImageSendMessage(
                            original_content_url='https://res.cloudinary.com/lwyuki/image/upload/v1623558988/static/img/illustration/%E5%AE%9A%E4%BD%8D%E6%90%9C%E5%B0%8B2_kjnkn9.png', 
                            preview_image_url='https://res.cloudinary.com/lwyuki/image/upload/v1623558988/static/img/illustration/%E5%AE%9A%E4%BD%8D%E6%90%9C%E5%B0%8B2_kjnkn9.png'))
                        line_bot_api.reply_message(event.reply_token, message)
                    except:
                        line_bot_api.reply_message (event.reply_token, TextSendMessage(text='發生錯誤!'))
                if backdata.get('illuMenu') == 'True':
                    try:
                        message = []
                        message.append(ImageSendMessage(
                            original_content_url='https://res.cloudinary.com/lwyuki/image/upload/v1623558987/static/img/illustration/%E8%8F%9C%E5%96%AE%E6%90%9C%E5%B0%8B1_mv9g6m.png', 
                            preview_image_url='https://res.cloudinary.com/lwyuki/image/upload/v1623558987/static/img/illustration/%E8%8F%9C%E5%96%AE%E6%90%9C%E5%B0%8B1_mv9g6m.png'))
                        message.append(ImageSendMessage(
                            original_content_url='https://res.cloudinary.com/lwyuki/image/upload/v1623558993/static/img/illustration/%E8%8F%9C%E5%96%AE%E6%90%9C%E5%B0%8B2_buacuy.png', 
                            preview_image_url='https://res.cloudinary.com/lwyuki/image/upload/v1623558993/static/img/illustration/%E8%8F%9C%E5%96%AE%E6%90%9C%E5%B0%8B2_buacuy.png'))
                        line_bot_api.reply_message(event.reply_token, message)
                    except:
                        line_bot_api.reply_message (event.reply_token, TextSendMessage(text='發生錯誤!'))
                if backdata.get('illuBus') == 'True':
                    try:
                        message = []
                        message.append(ImageSendMessage(
                            original_content_url='https://res.cloudinary.com/lwyuki/image/upload/v1623558987/static/img/illustration/%E5%85%AC%E8%BB%8A%E8%B3%87%E8%A8%8A1_sbn6tb.png', 
                            preview_image_url='https://res.cloudinary.com/lwyuki/image/upload/v1623558987/static/img/illustration/%E5%85%AC%E8%BB%8A%E8%B3%87%E8%A8%8A1_sbn6tb.png'))
                        message.append(ImageSendMessage(
                            original_content_url='https://res.cloudinary.com/lwyuki/image/upload/v1623558987/static/img/illustration/%E5%85%AC%E8%BB%8A%E8%B3%87%E8%A8%8A2_p6ebqu.png', 
                            preview_image_url='https://res.cloudinary.com/lwyuki/image/upload/v1623558987/static/img/illustration/%E5%85%AC%E8%BB%8A%E8%B3%87%E8%A8%8A2_p6ebqu.png'))
                        line_bot_api.reply_message(event.reply_token, message)
                    except:
                        line_bot_api.reply_message (event.reply_token, TextSendMessage(text='發生錯誤!'))
                if backdata.get('illuUbike') == 'True':
                    try:
                        message = ImageSendMessage(
                            original_content_url='https://res.cloudinary.com/lwyuki/image/upload/v1623558993/static/img/illustration/Ubike%E8%B3%87%E8%A8%8A_sifnom.png', 
                            preview_image_url='https://res.cloudinary.com/lwyuki/image/upload/v1623558993/static/img/illustration/Ubike%E8%B3%87%E8%A8%8A_sifnom.png')
                        line_bot_api.reply_message(event.reply_token, message)
                    except:
                        line_bot_api.reply_message (event.reply_token, TextSendMessage(text='發生錯誤!'))
                if backdata.get('illuCamp') == 'True':
                    try:
                        message = ImageSendMessage(
                            original_content_url='https://res.cloudinary.com/lwyuki/image/upload/v1623558994/static/img/illustration/%E6%A0%A1%E5%9C%92%E5%9C%B0%E5%9C%96_qhywm2.png', 
                            preview_image_url='https://res.cloudinary.com/lwyuki/image/upload/v1623558994/static/img/illustration/%E6%A0%A1%E5%9C%92%E5%9C%B0%E5%9C%96_qhywm2.png')
                        line_bot_api.reply_message(event.reply_token, message)
                    except:
                        line_bot_api.reply_message (event.reply_token, TextSendMessage(text='發生錯誤!'))

            
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

