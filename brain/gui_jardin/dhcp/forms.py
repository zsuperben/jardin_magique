# forms file
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from models import *


class configform(ModelForm):
    class Meta:
        model = Config

networkformset = inlineformset_factory(Config, Networks)
netbootformset = inlineformset_factory(Config, Netboot)
