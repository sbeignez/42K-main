from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout


class RaceListFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(RaceListFormHelper, self).__init__(*args, **kwargs)
        self.form_method = 'get'
        self.field_template = 'bootstrap3/layout/inline_field.html'
        self.form_class = 'form-inline'
        self.layout = Layout(
            'country', StrictButton('Submit', type='submit', css_class='btn-primary'))


