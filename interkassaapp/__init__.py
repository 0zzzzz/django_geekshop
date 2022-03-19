from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

__version__ = '1.0.0'

default_app_config = 'interkassaapp.Config'


class Config(AppConfig):
    name = 'interkassaapp'
    verbose_name = _("Interkassa Merchant")
    label = 'interkassaapp'
