from django import forms
from delve import models
from dal import autocomplete
from django.conf import settings
from haystack.forms import SearchForm

# 2FA (twilio/authy)
# ============================================================
import phonenumbers
from authy.api import AuthyApiClient
from phonenumbers.phonenumberutil import NumberParseException
authy_api = AuthyApiClient(settings.ACCOUNT_SECURITY_API_KEY)
# ============================================================

class DateRangeSearchForm(SearchForm):
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(DateRangeSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        # Check to see if a start_date was chosen.
        if self.cleaned_data['start_date']:
            sqs = sqs.filter(pub_date__gte=self.cleaned_data['start_date'])

        # Check to see if an end_date was chosen.
        if self.cleaned_data['end_date']:
            sqs = sqs.filter(pub_date__lte=self.cleaned_data['end_date'])

        return sqs
# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     class Meta():
#         model = User
#         fields = ('first_name', 'last_name', 'username','password','email')
        
class AccountActionForm(forms.Form):
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea,
    )
    send_email = forms.BooleanField(
        required=False,
    )
    @property
    def email_subject_template(self):
        return 'email/account/notification_subject.txt'
    @property
    def email_body_template(self):
        raise NotImplementedError()
    def form_action(self, account, user):
        raise NotImplementedError()
    def save(self, account, user):
        try:
            account, action = self.form_action(account, user)
        except errors.Error as e:
            error_message = str(e)
            self.add_error(None, error_message)
            raise
        if self.cleaned_data.get('send_email', False):
            send_email(
                to=[account.user.email],
                subject_template=self.email_subject_template,
                body_template=self.email_body_template,
                context={
                    "account": account,
                    "action": action,
                }
            )
        return account, action



class CancerForm(forms.ModelForm):
    cancers = forms.ModelChoiceField(
        required=False,
        label='',
        queryset=models.Cellline.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='cancer-autocomplete',
            attrs={
                # for styling
                'class' : 'cancerForm',
                # Set some placeholder
                'data-placeholder': 'Cancer or Cell Line ...',
                # Only trigger autocompletion after 3 characters have been typed
                'data-minimum-input-length': 1,
            }),
    )

    class Meta:
        model = models.Cellline
        fields = []

class CellLineForm(forms.ModelForm):
    celllines = forms.ModelChoiceField(
        required=False,
        label='',
        queryset=models.Cellline.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='cell-autocomplete',
            attrs={
                # for styling
                'class' : 'CellLineForm',
                # Set some placeholder
                'data-placeholder': 'Enter Cell Line ...',
                # Only trigger autocompletion after 3 characters have been typed
                'data-minimum-input-length': 1,
            }),
    )

    class Meta:
        model = models.Cellline
        fields = []

class DrugForm(forms.ModelForm):
    drugs = forms.ModelChoiceField(
        required=False,
        label='',
        queryset=models.Drug.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='ic50-autocomplete',
            attrs={
                # for styling
                'class' : 'ic50Form mr-2',
                # Set some placeholder
                'data-placeholder': 'Drug or Cell Line ...',
                # Only trigger autocompletion after 1 characters have been typed
                'data-minimum-input-length': 1,
            }),
    )

    class Meta:
        model = models.Drug
        fields = []

# To be replaced
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = models.Profile
        fields = ('first_name', 'last_name','password','email')



# New forms for custom model WITH 2FA (using twilio/authy)

class BootstrapInput(forms.TextInput):
    def __init__(self, placeholder, size=12, *args, **kwargs):
        self.size = size
        super(BootstrapInput, self).__init__(attrs={
            'class': 'form-control input-sm',
            'placeholder': placeholder
        })

    def bootwrap_input(self, input_tag):
        classes = 'col-xs-{n} col-sm-{n} col-md-{n}'.format(n=self.size)

        return '''<div class="{classes}">
                    <div class="form-group">{input_tag}</div>
                  </div>
               '''.format(classes=classes, input_tag=input_tag)

    def render(self, *args, **kwargs):
        input_tag = super(BootstrapInput, self).render(*args, **kwargs)
        return self.bootwrap_input(input_tag)


class BootstrapPasswordInput(BootstrapInput):
    input_type = 'password'
    template_name = 'django/forms/widgets/password.html'


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('first_name', 'last_name', 'email', 'password')
        widgets = {
            'first_name': BootstrapInput('First Name'),
            'last_name': BootstrapInput('Last Name'),
            'email': BootstrapInput('Email Address'),
            'password': BootstrapPasswordInput('Password', size=6),
        }

    country_code = forms.CharField(
        widget=BootstrapInput('Country Code', size=6))
    phone_number = forms.CharField(
        widget=BootstrapInput('Phone Number', size=6))
    confirm_password = forms.CharField(
        widget=BootstrapPasswordInput('Confirm Password', size=6))


    def clean_country_code(self):
        country_code = self.cleaned_data['country_code']
        if not country_code.startswith('+'):
            country_code = '+' + country_code
        return country_code

    def clean(self):
        data = self.cleaned_data
        if data['password'] != data['confirm_password']:
            self.add_error(
                'password',
                'Password and confirmation did not match'
            )

        phone_number = data['country_code'] + data['phone_number']
        print('Phoney number: {}'.format(phone_number))
        try:
            phone_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(phone_number):
                self.add_error('phone_number', 'Invalid phone number')
                print('invalid phone number')
        except NumberParseException as e:
            print('phone_number', e)
            self.add_error('phone_number', e)


class TokenVerificationForm(forms.Form):
    token = forms.CharField(
        required=True,
        widget=BootstrapInput('Input token received via SMS')
    )

    def is_valid(self, authy_id):
        self.authy_id = authy_id
        return super(TokenVerificationForm, self).is_valid()

    def clean(self):
        token = self.cleaned_data['token']
        verification = authy_api.tokens.verify(self.authy_id, token)
        if not verification.ok():
            self.add_error('token', 'Invalid token')

# class ML_MODEL_FORM(forms.ModelForm):
#         models = forms.ModelChoiceField(
#         required=False,
#         label='',
#         queryset=M2M_MODELS.Models.objects.all(),
#         widget=autocomplete.ModelSelect2(
#             url='ic50-autocomplete',
#             attrs={
#                 # for styling
#                 'class' : 'ic50Form mr-2',
#                 # Set some placeholder
#                 'data-placeholder': 'Drug or Cell Line ...',
#                 # Only trigger autocompletion after 1 characters have been typed
#                 'data-minimum-input-length': 1,
#             }),
#     )

#     class Meta:
#         model = models.Drug
#         fields = []