from linebot.models import CarouselColumn,URIAction

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