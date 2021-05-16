# CYIM-linebot-finalproject
 為大一新生設計的生活輔助系統

` 已部署到Heroku` `使用Cloudinary`


#### 📌主題：
    1. 食物：飲料店、午餐、早午餐...
    2. 交通：公車、Ubike (站牌)
    3. 選課：選課大全



#### 📌期望功能：
    1. 食物：查詢菜單、隨機找店家、…(其他功能)
    2. 交通：公車資訊、Ubike資訊、校園地圖
    3. 選課：課程評論



</br>

---

</br>

### 筆記

#### Webhook URL in Line
`https://[ Heroku app Name ].herokuapp.com/callback`

#### 建立虛擬環境
（若是projectvenv目錄已經存在，就不需要建立：`python -m venv projectvenv` ）

`cd projectvenv`

`scripts\activate`

#### 安裝套件

`cd..` <font color=#008000>#移到主目錄下</font>  
`pip install -r requirements.txt` <font color=#008000>#安裝requirements文件中的套件</font>  

#### 離開虛擬環境
`deactivate`

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
    │  replyCarousel.py
    │
    └─__pycache__
```



參考資料：
* https://acupun.site/lecture/django/index.htm#chp20
* https://cruelshare.com/line-bot-second/#%E8%A8%AD%E5%AE%9A%E6%AA%94%E4%BD%8D%E7%BD%AE