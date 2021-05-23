from linebot.models import messages
import requests
import json
from cyimapp.myLibrary.distance import haversine #計算距離
url = "https://data.tycg.gov.tw/opendata/datalist/datasetMeta/download?id=5ca2bfc7-9ace-4719-88ae-4034b9a5a55c&rid=a1b4714b-3b75-4ff8-a8f2-cc377e4eaa0f"
data = requests.get(url).json()

#取得所有桃園Ubike資料
def getUbikeInfo():
    
    listData =[]

    ubike_info = {} # 站代號: [此站資料,我的距離]

    for key, value in data["retVal"].items():
        sno = value["sno"]    #代號
        sna = value["sna"]    #場站名稱
        sbi = value["sbi"]    #可租借數
        bemp = value["bemp"]  #空位數

        lat = value["lat"]    #緯度
        lng = value["lng"]    #經度
        
        listData=[sno ,sna ,sbi ,bemp]
        ubike_info.update( {sno : listData})

    text ="站名\t  可租借數\t  可停車位\n"
    text +="----------------------------------------------"
    """
    for key, value in ubike_info:
        text += " \n"+value[1]+"\t "+value[2]+"\t "+value[3]
    """
    return ubike_info



#找離自己最近的10筆資料
def getUbikeData(myLongitude, myLatitude):
    
    listData =[]

    ubike_info = {} # 站代號: [此站資料,我的距離]

    for key, value in data["retVal"].items():
        sno = value["sno"]    #代號
        sna = value["sna"]    #場站名稱
        sbi = value["sbi"]    #可租借數
        bemp = value["bemp"]  #空位數

        lat = value["lat"]    #緯度
        lng = value["lng"]    #經度
        #print("NO.", sno,sna, " 可租借數:",sbi," 可停車位:",bemp)

        dist = haversine(myLongitude, myLatitude,float(lng),float(lat))
        listData=[sno ,sna ,sbi ,bemp ,dist]

        ubike_info.update( {sno : listData})
    ubike_info = sorted(ubike_info.items(), key=lambda d: d[1][4])[:10]    #取最近的10筆資料
    text ="站名\t  可租借數\t  可停車位\n"
    text +="----------------------------------------------"
    for key, value in ubike_info:
        text += " \n"+value[1]+"\t "+value[2]+"\t "+value[3]
    
    return text


'''
sno：站點代號
sna：場站名稱(中文)
tot：場站總停車格
sbi：場站目前車輛數量
sarea：場站區域(中文)
mday：資料更新時間
lat：緯度
lng：經度
ar：地(中文)
sareaen：場站區域(英文)
snaen：場站名稱(英文)
aren：地址(英文)
bemp：空位數量
act：全站禁用狀態
'''