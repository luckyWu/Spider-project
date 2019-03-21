

import requests
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3554.0 Safari/537.36'}
housedetail = 'https://hotels.ctrip.com/Domestic/tool/AjaxHote1RoomListForDetai1.aspx?psid=&MasterHotelID=4889292&hotel=4889292&EDM=F&roomId=&IncludeRoom=&city=2&showspothotel=T&supplier=&IsDecoupleSpotHotelAndGroup=F&contrast=0&brand=776&startDate=2019-03-14&depDate=2019-03-15&IsFlash=F&RequestTravelMoney=F&hsids=&IsJustConfirm=&contyped=0&priceInfo=-1&equip=&filter=&productcode=&couponList=&abForHuaZhu=&defaultLoad=T&esfiltertag=&estagid=&Currency=RMB&Exchange=1&TmFromList=F&RoomGuestCount=1,1,0&eleven=2fd7e36b590e0f3a4223c8ef86005685240b57f4eb6b31075d421b348df2edad&callback=CASiWEoMauSCdlEnxSc&_=1552543021451'
h22='https://hotels.ctrip.com/Domestic/tool/AjaxHote1RoomListForDetai1.aspx?psid=&MasterHotelID=4889292&hotel=4889292&EDM=F&roomId=&IncludeRoom=&city=2&showspothotel=T&supplier=&IsDecoupleSpotHotelAndGroup=F&contrast=0&brand=776&startDate=2019-03-14&depDate=2019-03-15&IsFlash=F&RequestTravelMoney=F&hsids=&IsJustConfirm=&contyped=0&priceInfo=-1&equip=&filter=&productcode=&couponList=&abForHuaZhu=&defaultLoad=T&esfiltertag=&estagid=&Currency=RMB&Exchange=1&TmFromList=F&RoomGuestCount=1,1,0&eleven=29bd74d6cfe7f5c2481e87e31377c743a1b86c7f05936de421cb00ec96813796&callback=CASoNhnGumtCSKRugET&_=1552553480978'
url = 'http://hotel.qunar.com/city/sanya/q-%E8%9C%88%E6%94%AF%E6%B4%B2%E5%B2%9B#fromDate=2019-03-18&cityurl=sanya&from=hotellist&toDate=2019-03-19&QHFP=ZSL_A16C2CA7&bs=&bc=%E4%B8%89%E4%BA%9A'
from bs4 import BeautifulSoup
# table border="0" cellspacing="0" cellpadding="0" summary="详情页酒店房型列表" id="J_RoomListTbl"
meituanurl = 'https://hotel.meituan.com/beijing/'

res = requests.get(url=meituanurl,headers=header)
print(res.status_code)
print(res.content.decode('utf-8'))
# n= 0
# while True:
# 	n = n+1
# 	res = requests.get(url)
# 	s = res.status_code
# 	# res = BeautifulSoup(res.text, 'lxml')
# 	# print(res.title.string)
# 	if s != 200:
# 		print(s,n)
# 		break