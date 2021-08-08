import json

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


class CreateBillView(View):
    def post(self, request, *args, **kwargs):
        try:
            comment = request.POST.get('comment', '')
            amount = float(request.POST['amount'])
            amount = round(amount, 2)
            site = request.POST['site']

            bill = Bill.objects.create(comment=comment, amount=amount, site=site)

            response = {
                'id': bill.id,
                'payUrl': bill.get_url()
            }

            return HttpResponse(json.dumps(response), content_type='application/json', status=201)
        except:
            return HttpResponse('Something went wrong!', status=400)


@api_view(['POST'])
def SuccessBillView(request):
    try:
        data = request.POST['bill']

        len_QIWI_DB_VERSION = len(f'{settings.QIWI_DB_VERSION}_')
        bill_id = int(data['billId'][len_QIWI_DB_VERSION:])

        bill = Bill.objects.get(id=bill_id)
        bill.status = data['status']['value']
        bill.save()

        bill.success()

        return Response({'status': 'ok'}, status=202)
    except:
        return Response({'status': 'something went wrong'}, status=500)


# class SuccessBillView(View):
#     def post(self, request, *args, **kwargs):
#         try:
#             data = request.POST['bill']
#
#             len_QIWI_DB_VERSION = len(f'{settings.QIWI_DB_VERSION}_')
#             bill_id = int(data['billId'][len_QIWI_DB_VERSION:])
#
#             bill = Bill.objects.get(id=bill_id)
#             bill.status = data['status']['value']
#             bill.save()
#
#             bill.success()
#
#             return HttpResponse('Ok!', status=202)
#         except:
#             return HttpResponse('Something went wrong!', status=500)
