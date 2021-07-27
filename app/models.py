from django.db import models

# Create your models here.


def qr_path(instance, filename):
    """
    * Path to the image qr code
    """
    return f"{instance.info.first_name + instance.info.last_name}_logo/{filename}"


class Contact(models.Model):
    last_name = models.CharField("Nom", max_length=30)
    first_name = models.CharField("Prénom(s)", max_length=30)
    gender = models.CharField(
        "Sexe", choices=[("h", "Homme"), ("f", "Femme")], max_length=1
    )
    work_place = models.CharField("Établissement", max_length=30)
    job = models.CharField(
        "UFR",
        max_length=30,
    )
    phone = models.CharField("Téléphone", max_length=30, unique=True)
    email = models.CharField("Courriel", max_length=30, unique=True)
    field = models.CharField("Département", max_length=30)


class QRCodeImage(models.Model):
    image = models.ImageField(upload_to=qr_path)
    info = models.ForeignKey(Contact, on_delete=models.CASCADE)
