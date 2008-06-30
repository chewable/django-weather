from bpaulson.weather.models import *
from django import template
from django.template import RequestContext

register = template.Library()




def get_weather():
		wx = Current.objects.get(pk=1)
		weather = wx.getInfo(wx)
		return {'weather': weather}

def quicklook(data,unitSpeed,daynum):
	cTime = time.strftime("%H", time.localtime(time.time()))
	if cTime > 14:
		block1 = {'header':'Tonight','temp':data['forecast'][0]['low'],'sunset':data['forecast'][0]['sunset'],'icon':data['forecast'][0]['night']['icon'],'type':data['forecast'][0]['night']['type']}
		block2 = {'header':data['forecast'][1]['Day'],'temp':data['forecast'][1]['high'],'sunset':data['forecast'][0]['sunset'],'sunrise':data['forecast'][1]['sunrise'],'icon':data['forecast'][1]['day']['icon'],'type':data['forecast'][1]['day']['type']}
	else:
		block1 = {'header':'Today','temp':data['forecast'][0]['high'],'sunset':data['forecast'][0]['sunrise'],'icon':datadata['forecast'][0]['day']['icon'],'type':data['forecast'][0]['day']['type']}
		block2 = {'header':'Tonight','temp':data['forecast'][0]['low'],'sunset':data['forecast'][0]['sunset'],'sunrise':data['forecast'][0]['sunrise'],'icon':data['forecast'][1]['night']['icon'],'type':data['forecast'][1]['night']['type']}	
		
	return {"block1":block1,"block2":block2}
	
def daily(data,daynum):
	return {
	'day_num': daynum,
	'day':data['Day'],
	'day_hi':data['high'],
	'day_icon':data['day']['icon'],
	'day_type':data['day']['type']
	}
	
def forecast(data,unitSpeed,daynum):
	return {
	'day_num': daynum,
	'unitspeed':unitSpeed,
	'day':data['Day'],
	'date':data['Date'],
	'day_hi':data['high'],
	'day_icon':data['day']['icon'],
	'day_humidity':data['day']['humidity'],
	'day_type':data['day']['type'],
	'day_pop':data['day']['pop'],
	'day_wind_direction':data['day']['wind']['direction'],
	'day_wind_speed':data['day']['wind']['speed'],
	'day_wind_gusts':data['day']['wind']['gusts'],
	'night_low':data['low'],
	'night_icon':data['night']['icon'],
	'night_humidity':data['night']['humidity'],
	'night_type':data['night']['type'],
	'night_pop':data['night']['pop'],
	'night_wind_direction':data["night"]["wind"]["direction"],
	'night_wind_speed':data['night']['wind']['speed'],
	'night_wind_gusts':data['night']['wind']['gusts'],
	}


register.inclusion_tag('weather/daily.html')(daily)
register.inclusion_tag('weather/quicklook.html')(quicklook)
register.inclusion_tag('weather/details.html')(forecast)
register.inclusion_tag('weather/embed.html')(get_weather)