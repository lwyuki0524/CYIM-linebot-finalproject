from linebot.models import CarouselColumn,URIAction,FlexSendMessage
from linebot.models.flex_message import BubbleContainer, CarouselContainer

def FlexReply(webUrl,imgUrl,name,address):

    bubble = {
      "type": "bubble",
      "header": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "image",
              "url": imgUrl,
              "size": "full",
              "aspectMode": "cover",
              "aspectRatio": "150:120",
              "gravity": "center",
              "flex": 1
            },
            {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": name,
                  "position": "relative",
                  "align": "center",
                  "offsetTop": "45%",
                  "size": "25px",
                  "adjustMode": "shrink-to-fit",
                  "weight": "bold",
                  "color": "#ffffffdf"
                }
              ],
              "backgroundColor": "#00000060",
              "position": "absolute",
              "offsetBottom": "0px",
              "offsetStart": "0px",
              "offsetEnd": "0px",
              "paddingAll": "20px",
              "offsetTop": "0px"
            }
          ]
        }
      ],
      "paddingAll": "0px"
    },
      "body": {
        "backgroundColor": "#ffffff",
        "contents": [
          {
            "contents": [
              {
                "contents": [
                  {
                    "color": "#00000077",
                    "offsetStart": "1px",
                    "offsetTop": "1px",
                    "position": "absolute",
                    "size": "25px",
                    "text": "▎",
                    "type": "text"
                  },
                  {
                    "color": "#ffcc00",
                    "position": "absolute",
                    "size": "25px",
                    "text": "▎",
                    "type": "text"
                  },
                  {
                    "color": "#000000",
                    "offsetStart": "20px",
                    "size": "24px",
                    "text": name,
                    "type": "text",
                    "weight": "bold",
                    "wrap": True
                  }
                ],
                "layout": "vertical",
                "spacing": "sm",
                "type": "box"
              },
              {
                "contents": [
                  {
                    "color": "#000000",
                    "size": "sm",
                    "text": address,
                    "type": "text",
                    "weight": "bold",
                    "wrap": True
                  }
                ],
                "layout": "vertical",
                "margin": "sm",
                "paddingAll": "10px",
                "type": "box"
              }
            ],
            "layout": "vertical",
            "type": "box"
          },
          {
            "contents": [
              {
                "backgroundColor": "#E5AF00",
                "contents": [
                  {
                    "action": {
                      "label": "  ",
                      "type": "uri",
                      "uri": webUrl
                    },
                    "adjustMode": "shrink-to-fit",
                    "color": "#ffffff",
                    "height": "sm",
                    "margin": "5px",
                    "position": "relative",
                    "style": "link",
                    "type": "button"
                  }
                ],
                "cornerRadius": "20px",
                "layout": "horizontal",
                "margin": "10px",
                "position": "absolute",
                "type": "box",
                "width": "100%"
              },
              {
                "contents": [
                  {
                    "align": "center",
                    "color": "#ffffff",
                    "size": "20px",
                    "text": "網　站",
                    "type": "text",
                    "weight": "bold",
                    "action": {
                      "type": "uri",
                      "uri": webUrl
                    }
                  }
                ],
                "cornerRadius": "20px",
                "layout": "vertical",
                "margin": "10px",
                "offsetBottom": "4px",
                "position": "relative",
                "type": "box",
                "width": "50%",
                "offsetStart": "25%"
              }
            ],
            "layout": "vertical",
            "position": "relative",
            "type": "box",
            "width": "100%",
            "offsetTop": "sm",
            "height": "40%"
          }
        ],
        "layout": "vertical",
        "paddingAll": "20px",
        "type": "box"
      },
      "styles": {
        "hero": {
          "backgroundColor": "#ffffff"
        }
      }
    }
    message = FlexSendMessage(alt_text='FlexSendMessage', contents=bubble) 
    return message

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