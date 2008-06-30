# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from bpaulson.weather.models import *
import datetime
import time

# Create your views here.
def index(request):
		wx = Current.objects.get(pk=1)
		weather = wx.getInfo(wx)
		currenttime = time.strftime("%H:%M:%p", time.localtime(time.time()))
		return render_to_response('weather/index.html', {'weather': weather,'currenttime':currenttime},context_instance=RequestContext(request))