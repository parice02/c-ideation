from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
import qrcode
import json

from qrcodeserve import settings
from .forms import ContactForm
from .models import Contact, QRCodeImage


# Create your views here.


def index(request):
    contact = ContactForm(data=request.POST if request.POST else None)
    if request.POST:
        if contact.is_valid():
            contact.save()
            _contact = serializers.serialize('json', [contact.instance])
            _contact = json.loads(_contact)
            _contact = _contact[0]
            _contact['fields']["id"] = _contact['pk']
            _contact = _contact['fields']
            _contact = {"id": _contact['id'],
                        'first_name': _contact['first_name'],
                        "last_name": _contact['last_name'],
                        "phone": _contact['phone']}
            data_str = json.dumps(_contact)
            qr_image = generate_qr(data_str)
            extention = 'png'
            p = _contact['first_name'] + \
                _contact['last_name'] + '.' + extention
            path = settings.MEDIA_ROOT / p
            qr_image.save(path, extention)

            return render(request, 'qrcode.html',
                          {'image': f'https://media.c-ideation.herokuapp.com/media/{p}'})
    return render(request, 'index.html', {'contact': contact})


def generate_qr(data):

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")
