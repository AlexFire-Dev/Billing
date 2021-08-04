from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, TemplateView, CreateView, UpdateView, RedirectView

from .models import *


class CreateBillView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        bill = get_object_or_404(Bill, id=self.BillId)
        return bill.get_url()

    def post(self, request, *args, **kwargs):
        comment = request.POST.get('comment')
        amount = float(request.POST.get('amount'))
        site = request.POST.get('site')

        try:
            bill = Bill.objects.create(comment=comment, amount=amount, site=site)
        except:
            return HttpResponse('Something went wrong!')

        self.BillId = bill.id
        return super(CreateBillView, self).post(self, request, *args, **kwargs)


class SuccessBillView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = request.POST['bill']

            len_QIWI_DB_VERSION = len('{settings.QIWI_DB_VERSION}_')
            bill_id = int(data['billId'][len_QIWI_DB_VERSION:])

            bill = Bill.objects.get(id=bill_id)
            bill.status = data['status']['value']
            bill.save()

            bill.success()

            return HttpResponse('Ok!')
        except:
            return HttpResponse('Something went wrong!')
