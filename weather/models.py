from django.db import models
from xml.dom.minidom import parse, parseString
import urllib2
import datetime
import time

class Current(models.Model):
    zipcode = models.CharField(maxlength=20)
    last_update = models.DateTimeField()
    weather_xml = models.TextField()

    def getInfo(self,wx):
        #wx = Current.objects.get(pk=1)
        ctime = time.time() - 1800
        if wx.last_update > datetime.datetime.fromtimestamp(ctime):
            xml =  wx.weather_xml
            weather = wx.getWeather(xml)
        else:
            xml = wx.getData()
            #wx = {'last_update':datetime.datetime.today(),'weather_xml':weather}
            wx.last_update = datetime.datetime.today()
            wx.weather_xml  = xml
            wx.zipcode = 81007
            wx.save()
            weather = wx.getWeather(xml)

        return weather

    def getData(self):
        """Connect to weather.com and get the weather as raw XML"""
        urlHandle = urllib2.urlopen('http://xoap.weather.com/weather/local/%s?cc=1&dayf=10&unit=%s' %(81007, 's'))
        return urlHandle.read()

    def getWeather(self,xml):
        self.currentConditions = {}
        self.forecast = {}
        dom = parseString(xml)
        for node in dom.childNodes[1].childNodes:
            if node.nodeName == 'cc':
                self._setCurrentConditions(node)

            if node.nodeName == 'head':
                self._setCurrentConditions(node)

            if node.nodeName == 'dayf':
                self._setForecast(node)

            if node.nodeName == 'loc':
                self._setCurrentConditions(node)

            self.currentConditions['forecast'] = self.forecast
        return self.currentConditions

    def _setCurrentConditions(self, node):
        for elem in node.childNodes:
            if elem.nodeName == 'ut':
                self.currentConditions['unitTemp'] = elem.firstChild.data   

            if elem.nodeName == 'ud':
                self.currentConditions['unitDistance'] = elem.firstChild.data

            if elem.nodeName == 'us':
                self.currentConditions['unitSpeed'] = elem.firstChild.data

            if elem.nodeName == 'up':
                self.currentConditions['unitPrecip'] = elem.firstChild.data

            if elem.nodeName == 'ur':
                self.currentConditions['unitPressure'] = elem.firstChild.data

            if elem.nodeName == 'suns':
                self.currentConditions['sunset'] = elem.firstChild.data

            if elem.nodeName == 'icon':
                self.currentConditions['icon'] = elem.firstChild.data

            if elem.nodeName == 'sunr':
                self.currentConditions['sunrise'] = elem.firstChild.data

            if elem.nodeName == 'lsup':
                self.currentConditions['observed'] = elem.firstChild.data

            if elem.nodeName == 'obst':
                self.currentConditions['cityname'] = elem.firstChild.data

            if elem.nodeName == 'tmp':
                self.currentConditions['temperature'] = elem.firstChild.data

            if elem.nodeName == 't':
                self.currentConditions['type'] = elem.firstChild.data

            if elem.nodeName == 'flik':
                self.currentConditions['feelslike'] = elem.firstChild.data

            if elem.nodeName == 'vis':
                self.currentConditions['visibility'] = elem.firstChild.data

            if elem.nodeName == 'hmid':
                self.currentConditions['humidity'] = elem.firstChild.data

            if elem.nodeName == 'dewp':
                self.currentConditions['dewpoint'] = elem.firstChild.data

            if elem.nodeName == 'bar':
                self.currentConditions['bar'] = {}
                for subelem in elem.childNodes:
                    if subelem.nodeName == 'r':
                        self.currentConditions['bar']['reading'] = subelem.firstChild.data

                    if subelem.nodeName == 'd':
                        self.currentConditions['bar']['direction'] = subelem.firstChild.data

            if elem.nodeName == 'uv':
                self.currentConditions['uv'] = {}
                for subelem in elem.childNodes:
                    if subelem.nodeName == 'i':
                        self.currentConditions['uv']['index'] = subelem.firstChild.data

                    if subelem.nodeName == 't':
                        self.currentConditions['uv']['risk'] = subelem.firstChild.data

            if elem.nodeName == 'wind':
                self.currentConditions['wind'] = {}
                for subelem in elem.childNodes:
                    if subelem.nodeName == 's':
                        self.currentConditions['wind']['speed'] = subelem.firstChild.data

                    if subelem.nodeName == 'gust':
                        self.currentConditions['wind']['gusts'] = subelem.firstChild.data

                    if subelem.nodeName == 'd':
                        self.currentConditions['wind']['degrees'] = subelem.firstChild.data

                    if subelem.nodeName == 't':
                        self.currentConditions['wind']['direction'] = subelem.firstChild.data

    def _setForecast(self, node):
        day = 0
        for elem in node.childNodes:
            if elem.nodeName == 'lsup':
                pass

            if elem.nodeName == 'day':
                self._setForecastDay(
                    elem, 
                    elem.attributes['d'].value,
                    elem.attributes['t'].value,
                    elem.attributes['dt'].value
                )

    def _setForecastDay(self, node, index, day, date):
        index = int(index)
        self.forecast[index] = {}
        self.forecast[index]['Day'] = day
        self.forecast[index]['Date'] = date

        for elem in node.childNodes:
            if elem.nodeName == 'hi':
                if elem.firstChild.data == 'N/A':
                    self.forecast[index]['high'] = 'NA'
                else:
                    self.forecast[index]['high'] = elem.firstChild.data

            if elem.nodeName == 'low':
                if elem.firstChild.data == 'N/A':
                    self.forecast[index]['low'] = 'NA'
                else:
                    self.forecast[index]['low'] = elem.firstChild.data

            if elem.nodeName == 'sunr':
                self.forecast[index]['sunrise'] = elem.firstChild.data

            if elem.nodeName == 'suns':
                self.forecast[index]['sunset'] = elem.firstChild.data

            if elem.nodeName == 'ppcp':
                self.forecast[index]['pop'] = elem.firstChild.data
                    
            if elem.nodeName == 'hmid':
                self.forecast[index]['humidity'] = elem.firstChild.data

            if elem.nodeName == 'hmid':
                self.forecast[index]['humidity'] = elem.firstChild.data

            if elem.nodeName == 'part':
                if elem.attributes['p'].value == 'd':
                    self.forecast[index]['day'] = {}
                    for subelem in elem.childNodes:
                        if subelem.nodeName == 't':
                            self.forecast[index]['day']['type'] = subelem.firstChild.data

                        if subelem.nodeName == 'icon':
                            self.forecast[index]['day']['icon'] = subelem.firstChild.data

                        if subelem.nodeName == 'ppcp':
                            self.forecast[index]['day']['pop'] = subelem.firstChild.data

                        if subelem.nodeName == 'hmid':
                            self.forecast[index]['day']['humidity'] = subelem.firstChild.data

                        if subelem.nodeName == 'wind':
                            self.forecast[index]['day']['wind'] = {}
                            for windelem in subelem.childNodes:
                                if windelem.nodeName == 's':
                                    self.forecast[index]['day']['wind']['speed'] = windelem.firstChild.data

                                if windelem.nodeName == 'gust':
                                    self.forecast[index]['day']['wind']['gusts'] = windelem.firstChild.data

                                if windelem.nodeName == 'd':
                                    self.forecast[index]['day']['wind']['degrees'] = windelem.firstChild.data

                                if windelem.nodeName == 't':
                                    self.forecast[index]['day']['wind']['direction'] = windelem.firstChild.data

                if elem.attributes['p'].value == 'n':
                    self.forecast[index]['night'] = {}
                    for subelem in elem.childNodes:
                        if subelem.nodeName == 't':
                            self.forecast[index]['night']['type'] = subelem.firstChild.data

                        if subelem.nodeName == 'icon':
                            self.forecast[index]['night']['icon'] = subelem.firstChild.data

                        if subelem.nodeName == 'ppcp':
                            self.forecast[index]['night']['pop'] = subelem.firstChild.data

                        if subelem.nodeName == 'hmid':
                            self.forecast[index]['night']['humidity'] = subelem.firstChild.data

                        if subelem.nodeName == 'wind':
                            self.forecast[index]['night']['wind'] = {}
                            for windelem in subelem.childNodes:
                                if windelem.nodeName == 's':
                                    self.forecast[index]['night']['wind']['speed'] = windelem.firstChild.data

                                if windelem.nodeName == 'gust':
                                    self.forecast[index]['night']['wind']['gusts'] = windelem.firstChild.data

                                if windelem.nodeName == 'd':
                                    self.forecast[index]['night']['wind']['degrees'] = windelem.firstChild.data

                                if windelem.nodeName == 't':
                                    self.forecast[index]['night']['wind']['direction'] = windelem.firstChild.data
