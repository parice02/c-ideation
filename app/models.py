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
    work_place = models.CharField("Établissement", max_length=50)
    job = models.CharField(
        "Domaine d'études",
        max_length=100,
    )
    phone = models.CharField("Téléphone", max_length=30, unique=True)
    email = models.CharField("Courriel", max_length=30, unique=True)
    field = models.CharField(
        "Niveau",
        max_length=10,
        choices=[
            ("licence", "Licence"),
            ("master", "Master"),
            ("doctorat", "Doctorat"),
        ],
    )
    # arrived_at = models.ManyToManyField(
    #        "Arrived", "visitors arrived", null=True, blank=True
    #    )


class QRCodeImage(models.Model):
    image = models.ImageField(upload_to=qr_path)
    info = models.ForeignKey(Contact, on_delete=models.CASCADE)


# class Arrived(models.Model):
#    arrived_at = models.DateTimeField()
