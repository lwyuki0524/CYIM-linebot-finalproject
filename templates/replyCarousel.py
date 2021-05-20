from linebot.models import CarouselColumn,URIAction,FlexSendMessage

def FlexReply(webUrl,imgUrl,name,address):
    bubble = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": imgUrl,
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
            "type": "uri",
            "uri": imgUrl
            }
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": name,
                    "align": "start"
                },
                {
                    "type": "text",
                    "text": address,
                    "align": "start"
                }
                ]
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                "type": "uri",
                "label": "網站",
                "uri": webUrl
                }
            },
            {
                "type": "spacer",
                "size": "sm"
            }
            ],
            "flex": 0
        }
    }

    #message = FlexSendMessage(alt_text='Flex', contents=bubble) 
    return bubble

def CarouselReply(webUrl,imgUrl,name,address):
    message = CarouselColumn(
        thumbnail_image_url=imgUrl,
        title=name,
        text=address,
        actions=[
            URIAction(
                label='網站',
                uri=webUrl
            )
        ]
    )
    return message