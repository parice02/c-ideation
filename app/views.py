from django.shortcuts import render
from django.core import serializers
from django.db.models import Q
import qrcode
import json
from django.core.files.uploadedfile import SimpleUploadedFile

import io

# from rest_framework.views import APIView
# from rest_framework.parsers import JSONParser
# from rest_framework import viewsets, permissions
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response
# from django.http import Http404

from .forms import ContactForm, QRCodeForm, RecoveryInfo
from .models import QRCodeImage

# Create your views here.


def index(request):
    contact = ContactForm(data=request.POST if request.POST else None)
    if request.method == "POST":
        if contact.is_valid():
            contact.save()
            _contact = serializers.serialize("json", [contact.instance])
            _contact = json.loads(_contact)
            _contact = _contact[0]
            _contact["fields"]["id"] = _contact["pk"]
            _contact = _contact["fields"]
            _contact["api"] = "ideation_camp_ujkz"
            data_str = json.dumps(_contact)
            qr_image = generate_qr(data_str)
            file_name = str(_contact["id"]) + "-" + _contact["phone"] + ".png"

            image_buffer = io.BytesIO()
            qr_image.save(image_buffer, "png")
            byte_img = image_buffer.getvalue()

            qr_code = QRCodeForm(
                data={"info": contact.instance},
                files={"image": SimpleUploadedFile(file_name, byte_img)},
            )
            if qr_code.is_valid():
                qr_code.save()

            return render(
                request,
                "qrcode.html",
                {"image": qr_code.instance},
            )
    return render(request, "index.html", {"contact": contact})


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


def recover_qrcode(request):
    """ """
    recuperation = RecoveryInfo(data=request.POST if request.POST else None)
    if request.method == "POST":
        if recuperation.is_valid():
            field = recuperation.cleaned_data.get("field")
            c = QRCodeImage.objects.get(Q(info__phone=field) | Q(info__email=field))
            return render(request, "qrcode.html", {"image": c})
    return render(request, "recovery.html", {"recuperation": recuperation})


# def check_visitor(request):
#    if request.method == "GET":
#        if "api" in request.GET and request.GET["api"] == "ideation_camp_2021":
#            pk = request.GET["pk"]
