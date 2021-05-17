from django.shortcuts import render
from cyimapp.models import foodTable
#from finalproject.settings import BASE_DIR
from django.conf import settings
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage,TemplateSendMessage,CarouselTemplate,QuickReply, messages
from linebot.models import QuickReplyButton,MessageAction,LocationAction
from urllib import parse#中文URL轉碼
from templates import replyCarousel


# Create your views here.
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

#domain = 'https://0681cff91f49.ngrok.io'+'/' #本地端網域       #### 測試時請使用這個(註解下方的domain)####
domain = 'https://res.cloudinary.com/lwyuki/image/upload/v1'+'/'#### heroku網域(上傳github請使用這個) ####

# show 資料表
def listfoodTable(request):
    allfoods = foodTable.objects.all().order_by('id')
    return render(request, "listfoodTable.html", locals())

# 快速回覆
def quick_reply():
    message=TextSendMessage(
        text="請選擇功能：",
        quick_reply=QuickReply(
        items=[
            QuickReplyButton(action=MessageAction(label="時段推薦",text="/時段推薦")),#回傳文字
            QuickReplyButton(action=LocationAction(label="定位搜尋"))#傳回定位資訊
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
            url = domain+parse.quote(str(item.fMenuImage).encode('utf-8'))
            print(url)
            message = replyCarousel.CarouselReply(item.fUrl,url,item.fName,item.fAddress )
            columns.append(message)
        
        carousel_template_message = TemplateSendMessage(alt_text='Carousel template',
                                                        template=CarouselTemplate(columns=columns))
        return carousel_template_message
    else:
        return False
            
    
        

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
                    #如果收到/飲食區，傳快速回覆訊息
                    if event.message.text=="/飲食區" :
                        msg = quick_reply()
                        line_bot_api.reply_message(event.reply_token,msg )
                    #隨機推薦此時段的店家
                    elif event.message.text=="/時段推薦" :
                        print("/時段推薦")
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "還沒做...") )

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
                    print(event.message)
                    #傳回經緯度(測試用)
                    line_bot_api.reply_message(event.reply_token,
                    TextSendMessage(text = 'latitude：'+ str(event.message.latitude) + '\nlongitude：'+str(event.message.longitude)) )
            
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
