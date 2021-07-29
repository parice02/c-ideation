from django import forms
from django.db.models import Q
from crispy_forms.layout import Layout, Div, Submit, Reset, ButtonHolder, HTML
from crispy_forms.helper import FormHelper

from .models import Contact, QRCodeImage


class ContactForm(forms.ModelForm):
    """ """

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = True
        helper.disable_csrf = False
        helper.include_media = False
        helper.form_method = "POST"
        helper.form_id = "idform"
        helper.form_action = ""
        helper.label_class = "col-8 form-check-label"
        helper.layout = Layout(
            Div(
                Div(
                    Div("last_name", css_class="col"),
                    Div("first_name", css_class="col"),
                    css_class="row",
                ),
                Div(
                    Div("gender", css_class="col"),
                    Div("email", css_class="col"),
                    Div("phone", css_class="col"),
                    css_class="row",
                ),
                Div(
                    Div("work_place", css_class="col"),
                    Div("job", css_class="col"),
                    Div("field", css_class="col"),
                    css_class="row",
                ),
            ),
            ButtonHolder(
                Submit("submit", "Générer", css_class="btn mr-5"),
                Reset("reset", "Tout effacer", css_class="btn btn-warning mr-5"),
                HTML(
                    '<a class="btn btn-success" href={% url "recover_qrcode" %}>Récupérer son QRCode</a>'
                ),
                css_class="btn btn-group mt-5 ",
            ),
        )
        return helper

    class Meta:
        model = Contact
        exclude = ("id",)


class QRCodeForm(forms.ModelForm):
    """ """

    class Meta:
        model = QRCodeImage
        exclude = ("id",)


class RecoveryInfo(forms.Form):
    """ """

    field = forms.CharField(
        label="Numéro de téléphone ou courriel",
        max_length=100,
        widget=forms.TextInput(),
    )

    def clean(self):
        cleaned_data = super(RecoveryInfo, self).clean()
        field = cleaned_data.get("field")
        if field:
            c = Contact.objects.filter(Q(phone=field) | Q(email=field))
            if c.count() == 0:
                raise forms.ValidationError(
                    "Oops! Nous ne trouvons aucune correspondance.", code="invalid"
                )
            return cleaned_data
        raise forms.ValidationError(
            "Veuillez vérifier les information saisies.", code="invalid"
        )

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = True
        helper.disable_csrf = False
        helper.include_media = False
        helper.form_method = "POST"
        helper.form_id = "idform"
        helper.field_class = "form-control"
        helper.form_action = ""
        helper.label_class = ""
        helper.layout = Layout(
            Div("field", css_class="form-group"),
            ButtonHolder(
                Submit("submit", "Récupérer", css_class="btn btn-primary mr-5"),
                Reset("reset", "Tout effacer", css_class="btn btn-warning"),
                css_class="btn btn-group mt-5 ",
            ),
        )
        return helper
