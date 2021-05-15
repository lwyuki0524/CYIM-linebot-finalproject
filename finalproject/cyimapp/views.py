from django.shortcuts import render
from cyimapp.models import foodTable
#from finalproject.settings import BASE_DIR
from django.conf import settings
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage,TemplateSendMessage,CarouselTemplate

from urllib import parse#中文URL轉碼
from templates import replyCarousel


# Create your views here.
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


def listall(request):
    allfoods = foodTable.objects.all().order_by('id')
    return render(request, "listall.html", locals())


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
        
        columns=[]
        domain = 'https://9944aad41311.ngrok.io/'+'/' #網域
        
        for event in events:
            if isinstance(event, MessageEvent):
                
                if event.message.text=="/read foodTable" :
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(
                        text='https://liff.line.me/'+'1655990146-npeZ9k20') )
                else:
                    unit = foodTable.objects.filter( fTag = event.message.text ) #讀取一筆資料
                    if(unit):
                        print(unit)
                        for item in unit :
                            url = domain+parse.quote(str(item.fMenuImage).encode('utf-8'))
                            print(url)
                            
                            message = replyCarousel.CarouselReply(item.fUrl,url,item.fName,item.fAddress )
                            columns.append(message)
                        carousel_template_message = TemplateSendMessage(
                            alt_text='Carousel template',template=CarouselTemplate(columns=columns))
                        line_bot_api.reply_message(event.reply_token, carousel_template_message)
                        
                    else:
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = event.message.text) )
            
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
