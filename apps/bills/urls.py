from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy, include

from .views import *


urlpatterns = [
    path('create/', CreateBillView.as_view(), name='create-bill')
]
