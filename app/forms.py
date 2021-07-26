from django import forms
from crispy_forms.layout import Layout, Div, Submit, Reset, ButtonHolder
from crispy_forms.helper import FormHelper
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    """

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = True
        helper.disable_csrf = False
        helper.include_media = False
        helper.form_method = 'POST'
        helper.form_id = 'idform'
        helper.form_action = ''
        helper.label_class = 'col-8 form-check-label'
        helper.layout = Layout(
            Div(
                Div(
                    Div('last_name', css_class="col"),
                    Div('first_name', css_class="col"),
                    css_class="row"),
                Div(
                    Div('gender', css_class="col"),
                    Div('email', css_class="col"),
                    Div('phone', css_class="col"),
                    css_class="row"),
                Div(
                    Div('work_place', css_class="col"),
                    Div('job', css_class="col"),
                    Div('field', css_class="col"),
                    css_class="row"),
            ),
            ButtonHolder(
                Submit('submit', 'Générer', css_class='btn mr-5'),
                Reset('reset', 'Tout effacer', css_class='btn btn-warning'),
                css_class='btn btn-group mt-5 '),
        )
        return helper

    class Meta:
        model = Contact
        exclude = ('id',)
