from django.shortcuts import render
from django.core import serializers
import qrcode
import json
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import Http404

from .forms import ContactForm, QRCOdeForm


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
            _contact = {
                "id": _contact["id"],
                "api": "ideation_camp_2021",
                "phone": _contact["phone"],
            }
            data_str = json.dumps(_contact)
            qr_image = generate_qr(data_str)
            file_name = str(_contact["id"]) + _contact["phone"] + ".png"

            buf = io.BytesIO()
            qr_image.save(buf, "png")
            byte_img = buf.getvalue()

            qr_code = QRCOdeForm(
                data={"info": contact.instance},
                files={"image": SimpleUploadedFile(file_name, byte_img)},
            )
            print(qr_code.errors.as_json())
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


#def check_visitor(request):
#    if request.method == "GET":
#        if "api" in request.GET and request.GET["api"] == "ideation_camp_2021":
#            pk = request.GET["pk"]

