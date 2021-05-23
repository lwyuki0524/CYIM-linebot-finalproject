from django.shortcuts import render
from linebot.models.actions import PostbackAction, URIAction
from cyimapp.models import foodTable
from django.conf import settings
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage,TemplateSendMessage,CarouselTemplate,QuickReply, messages
from linebot.models import QuickReplyButton,MessageAction,LocationAction
from urllib import parse#中文URL轉碼
from templates import replyCarousel

from cyimapp.myLibrary.distance import haversine #計算距離
from cyimapp.myLibrary.real_ubike import getUbikeInfo #取得Ubike資訊
from datetime import datetime, time
import time
from random import sample

# Create your views here.
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

#domain = 'https://d211f4ba3888.ngrok.io'+'/' #本地端網域       #### 測試時請使用這個(註解下方的domain)####
domain = 'https://res.cloudinary.com/lwyuki/image/upload/v1'+'/'#### cloudinary網域(上傳github請使用這個) ####

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

# 隨機選店家
def randomFood(event):
    #從用戶傳的文字中擷取ftag關鍵字
    columns=[]
    filter_text = " "
    food_entry_list = list(foodTable.objects.all())  #先列出所有食物物件
    #從物件中一一取出fTag來比對使用者的文字
    for food_item in food_entry_list:  
        if food_item.fTag in event.message.text:
            print(event.message.text +" find "+ food_item.fTag)
            filter_text = food_item.fTag
    unit = foodTable.objects.filter( fTag = filter_text ) #過濾資料
    
    if unit.exists():
        print(unit)
        for item in unit :
            addCarouselItem(item,columns)

        #如果有5筆以上資料，隨機挑5筆
        if len(columns)>=5:
            columns = sample(columns,5)

        carousel_template_message = TemplateSendMessage(alt_text='Carousel template', template=CarouselTemplate(columns=columns))
        return carousel_template_message
    else:
        return False


# 輸入 要製作成 Carousel的物件，輸出Carousel物件集合 (最多5個)
def addCarouselItem(item,columns):
    url = domain+parse.quote(str(item.fMenuImage).encode('utf-8'))
    print(url)
    message = replyCarousel.CarouselReply(item.fUrl,url,item.fName,item.fAddress )
    columns.append(message)
    return None


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
             #傳回5筆以內有在營業的店家
            line_bot_api.reply_message(event.reply_token,TemplateSendMessage(
                alt_text='Carousel template',template=CarouselTemplate(columns=columns)) )


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

        #傳回5個最近的店家
        line_bot_api.reply_message(event.reply_token,TemplateSendMessage(
            alt_text='Carousel template',template=CarouselTemplate(columns=columns)) )
    return None



#Ubike 資訊
def searchUbike(request):
    ubikeInfo = getUbikeInfo()
    return render(request, "searchUbike.html", locals())


# 交通區快速回覆
def traffic_quick_reply():
    message=TextSendMessage(
        text="請選擇功能",
        quick_reply=QuickReply(
        items=[
            QuickReplyButton(action=MessageAction(label="公車資訊",text="/公車資訊")),#回傳文字
            QuickReplyButton(action=URIAction(label="Ubike資訊",uri='https://liff.line.me/1655990146-0DxGKVrq',
             alt_uri='https://liff.line.me/1655990146-0DxGKVrq')),#網頁連結
            ]
        )
    )
    return message

###交通區功能###
def trafficArea(event):
    if event.message.type=='text':    
    #如果收到/交通區，傳快速回覆訊息
        if event.message.text=='/交通區':
            line_bot_api.reply_message(event.reply_token,traffic_quick_reply() )

    #############
    #
    #
    #   todo
    #
    #
    #############
    return None



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


                    #以下為測試用#
                    #如果收到/foodTable，傳資料表(測試用)
                    elif event.message.text=="/foodTable" :
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(
                            text='https://liff.line.me/'+'1655990146-npeZ9k20') )
                    #如果收到分類的關鍵字，隨機傳店家資訊(測試用)
                    elif randomFood(event):
                        carousel_template_message=randomFood(event)
                        line_bot_api.reply_message(event.reply_token, carousel_template_message)
                    #鸚鵡回話
                    else:
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = event.message.text) )

                #定位訊息
                elif event.message.type=='location':
                    #進入飲食區功能
                    foodArea(event)
                    
            
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
