from django import forms
from configstore.forms import ConfigurationForm
from configstore.configs import ConfigurationInstance, register

class WeatherConfigurationForm(ConfigurationForm):
    partner_id = forms.CharField()
    license_key = forms.CharField()

register(ConfigurationInstance('weather', 'Weather', WeatherConfigurationForm))
