from django.shortcuts import render
from cyimapp.models import foodTable
#from finalproject.settings import BASE_DIR
from django.conf import settings
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage,ImageSendMessage,TemplateSendMessage,CarouselTemplate

from urllib import parse#中文URL轉碼
from templates import replyCarousel


# Create your views here.
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


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
        
        reply_arr=[]#暫存多則訊息(最多五則)
        columns=[]
        domain = 'https://b393b266aa4b.ngrok.io/' #網域
        
        for event in events:
            if isinstance(event, MessageEvent):
                try:
                    unit = foodTable.objects.filter( fTag = event.message.text ) #讀取一筆資料
                    if(unit):
                        print(unit)
                        for item in unit :
                            url = domain+parse.quote(str(item.fMenuImage).encode('utf-8'))
                            print(url)
                            
                            message = replyCarousel.CarouselReply(item.fUrl,url,item.fName,item.fAddress )
                            columns.append(message)
                            #reply_arr.append( TextSendMessage(text = item.fName+" 網址："+item.fUrl) )
                            #reply_arr.append( ImageSendMessage(original_content_url=url,preview_image_url=url)  )
                        carousel_template_message = TemplateSendMessage(
                            alt_text='Carousel template',template=CarouselTemplate(columns=columns))
                        line_bot_api.reply_message(event.reply_token, carousel_template_message)
                        
                    else:
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = event.message.text) )
                except:
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text = event.message.text) )
            
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
