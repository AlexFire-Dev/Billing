import json
import hmac

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, TemplateView, CreateView, UpdateView, RedirectView

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view


from .models import *


class IndexBillView(TemplateView):
    template_name = 'bills/index.html'


class CreateBillFormView(TemplateView):
    template_name = 'bills/create-bill-form.html'


@api_view(['POST'])
def CreateBillView(request):
    try:
        comment = request.data.get('comment', '')
        amount = float(request.data.get('amount', '1.00'))
        amount = round(amount, 2)
        site = request.POST.get('site', '')

        bill = Bill.objects.create(comment=comment, amount=amount, site=site)

        response = {
            'id': bill.id,
            'payUrl': bill.get_url()
        }

        return Response(response, status=201)
    except:
        return Response({'status': 'something went wrong'}, status=400)


class SuccessBillView(View):
    def post(self, request, *args, **kwargs):
        import hmac
        import hashlib

        try:
            data = request.POST['bill']

            currency = data['amount']['currency']
            value = data['amount']['value']
            billId = data['billId']
            siteId = data['siteId']
            status = data['status']['value']

            secret_key = bytes(settings.QIWI_SECRET_KEY)
            message = bytes(f'{currency}|{value}|{billId}|{siteId}|{status}')
            my_signature = hmac.new(secret_key, message, hashlib.sha256).hexdigest()
            http_signature = request.headers.get('X-Api-Signature-SHA256').decode('UTF-8')

            if my_signature == http_signature:
                len_QIWI_DB_VERSION = len(f'{settings.QIWI_DB_VERSION}_')
                bill_id = int(data['billId'][len_QIWI_DB_VERSION:])

                bill = Bill.objects.get(id=bill_id)
                bill.status = data['status']['value']
                bill.save()

                bill.success()

                return HttpResponse('Ok!', status=200)
            else:
                return HttpResponse('Signature is incorrect!', status=409)
        except:
            return HttpResponse('Something went wrong!', status=500)
