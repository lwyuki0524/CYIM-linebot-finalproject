from linebot.models import CarouselColumn,URIAction,FlexSendMessage
from linebot.models.flex_message import BubbleContainer, CarouselContainer

def FlexReply(webUrl,imgUrl,name,address):
    bubble = {
      "type": "bubble",
      "size": "micro",
      "hero": {
        "type": "image",
        "url": imgUrl,
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": name,
            "weight": "bold",
            "size": "sm",
            "wrap": True
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": address,
                    "wrap": True,
                    "color": "#8c8c8c",
                    "size": "xs",
                    "flex": 5
                  }
                ]
              }
            ]
          },
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "網站",
              "uri": webUrl
            }
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      }
    } 
    message = CarouselContainer(alt_text='CarouselContainer', contents=bubble) 
    #print(message)
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