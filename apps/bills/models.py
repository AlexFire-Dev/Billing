import datetime
import json

import requests

from django.conf import settings
from django.db import models


class Bill(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=45, default='')
    amount = models.FloatField(default=1.00)
    status = models.CharField(max_length=15, null=True, blank=True)
    site = models.CharField(max_length=45)

    def get_url(self):
        try:
            headers = {
                'Authorization': f'Bearer {settings.QIWI_SECRET_KEY}',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }

            expirationDateTime = self.created_at + datetime.timedelta(days=2)
            expirationDateTime = expirationDateTime.strftime('%Y-%m-%dT%H:%M:%S+03:00')

            request_data = {
                'amount': {
                    'currency': 'RUB',
                    'value': str(round(self.amount, 2))
                },
                'comment': str(self.comment),
                'expirationDateTime': str(expirationDateTime),
            }
            request_data = json.dumps(request_data)
            response = requests.put(f'https://api.qiwi.com/partner/bill/v1/bills/{settings.QIWI_DB_VERSION}_{self.id}/', headers=headers, data=request_data)
            data = response.json()

            self.status = data['status']['value']
            return data['payUrl']
        except:
            return None

    def reject(self):
        try:
            headers = {
                'Authorization': f'Bearer {settings.QIWI_SECRET_KEY}',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }
            response = requests.post(f'https://api.qiwi.com/partner/bill/v1/bills/{settings.QIWI_DB_VERSION}_{self.id}/reject/', headers=headers)
            data = response.json()

            self.status = data['status']['value']
        except:
            return

    def success(self):
        import hmac
        import hashlib

        try:
            secret_key = bytes(settings.OPLATA_KEY)
            message = bytes(f'{self.id}|{self.status}|RUB|{self.amount}')
            signature = hmac.new(secret_key, message, hashlib.sha256).hexdigest()

            headers = {
                'Content-Type': 'application/json',
                'X-Api-Signature-SHA256': signature,
            }

            request_data = {
                'id': self.id,
                'status': self.status,
                'amount': {
                    'currency': 'RUB',
                    'value': str(self.amount)
                },
                'comment': self.comment,
            }

            request_data = json.dumps(request_data)

            response = requests.post(self.site, data=request_data, headers=headers)
            return response
        except:
            return None
