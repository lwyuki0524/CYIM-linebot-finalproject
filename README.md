# CYIM-linebot-finalproject
 為大一新生設計的生活輔助系統

` 部署到Heroku` `使用Cloudinary`  
django資料庫：https://cyim-finalproject.herokuapp.com/admin  
Heroku網站：https://dashboard.heroku.com/login  
Cloudinary網站：https://cloudinary.com/  

#### 📌主題：
    1. 食物：早餐、午餐、點心、飲料 
    2. 交通：公車、Ubike (站牌)



#### 📌期望功能：
    1. 食物：隨機找店家、定位搜尋、(額外功能：訂餐紀錄、查詢菜單)
    2. 交通：公車資訊、Ubike資訊、機車停車位、校園地圖



</br>

---

</br>

### 筆記

#### Webhook URL in Line
`https://[ Heroku app Name ].herokuapp.com/callback`


#### 本地端測試時
* 啟動ngrok：  
在cmd中，移動到專案資料夾內`cd [路徑]`，啟動`ngrok http 8000`
* 測試時需要改的資料：  
```
    1. settings.py (詳細請看檔案內註解說明)
    2. views.py (詳細請看檔案內註解說明)
    3. Line message api( Webhook URL：改成[ngrok提供的網域]/callback )
    4. Line login(LIFF)( Endpoint URL：前面改成[ngrok提供的網域]/ )
```
* 測試完畢要上傳github前，請將上方的設定改回來。
`( 第4點的[ngrok提供的網域] 要改回 https://cyim-finalproject.herokuapp.com )`

<br>

---
<br>

#### 下載此專案後

##### 1. 建立虛擬環境
（若是projectvenv目錄已經存在，就不需要建立，否則請輸入：`python -m venv projectvenv` ）

`cd projectvenv`

`scripts\activate`

##### 2. 安裝套件

`cd..` <font color=#008000>#移到主目錄下</font>  
`pip install -r requirements.txt` <font color=#008000>#安裝requirements文件中的套件</font>  

##### 3. 離開虛擬環境
`deactivate`

<br>

#### 檔案結構
```
.
│  .gitignore
│  db.sqlite3
│  manage.py
│  Procfile
│  README.md
│  requirements.txt
│  runtime.txt
│
├─cyimapp
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  tests.py
│  │  views.py
│  │  __init__.py
│  │
│  └─migrations
│
├─finalproject
│  │  asgi.py
│  │  prod_settings.py
│  │  settings.py
│  │  urls.py
│  │  wsgi.py
│  └─__init__.py
|
├─projectvenv
│  │  pyvenv.cfg
│  │
│  ├─Include
│  ├─Lib
│  │  └─site-packages
│  └─Scripts
│─static
│  └─img
│      └─menu
|─staticfiles
│  ├─admin
│  │  ├─css
│  │  ├─fonts
│  │  ├─img
│  │  └─js
│  ├─html
│  │      cloudinary_cors.html
│  └─js
└─templates
    │  listfoodTable.html
    └─ replyCarousel.py

```



參考資料：
* https://acupun.site/lecture/django/index.htm#chp20
* https://cruelshare.com/line-bot-second/#%E8%A8%AD%E5%AE%9A%E6%AA%94%E4%BD%8D%E7%BD%AE