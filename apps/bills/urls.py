from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy, include

from .views import *


urlpatterns = [
    path('create/', CreateBillView.as_view(), name='create-bill'),
    path('create/form/', login_required(CreateBillFormView.as_view()), name='create-bill-form'),

    path('success/', SuccessBillView.as_view(), name='success-bill'),

    path('', login_required(IndexBillView.as_view()), name='index')
]
