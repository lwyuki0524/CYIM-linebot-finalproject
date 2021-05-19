from math import sin, asin, cos, radians, fabs, sqrt

def haversine(lon1, lat1, lon2, lat2): # 經度1，緯度1，經度2，緯度2 （十進制度數）
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # 將十進制度數轉化為弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
 
    # haversine公式
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # 地球平均半徑，單位為公里
    return round(c * r * 1000,2)
