from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Div
import datetime
from django import forms
from app.models import RaceEvent


class RaceListFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(RaceListFormHelper, self).__init__(*args, **kwargs)
        self.form_method = 'get'
        self.field_template = 'bootstrap3/layout/inline_field.html'
        self.form_class = 'form-inline'
        self.layout = Layout(
            'date', 'country', StrictButton('Submit', type='submit', css_class='btn-primary'))


class NewRaceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
                Field('name', placeholder='Name', css_class='input-medium'),
                Field ('date', placeholder='Date', css_class='input-xlarge', initial=datetime.date.today),
            Div(
                Field('city', placeholder='City', rows='5', css_class='input-xlarge'),
                Field('country', placeholder='Country', css_class='input-xlarge'),
            ),
            StrictButton('Save', css_class='btn-default'),
        )
        self.helper.form_method = 'post'

        super(NewRaceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = RaceEvent
