# forms.py
from django import forms

class DateForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date'
    }))

class IDNumberForm(forms.Form):
    id_number = forms.CharField(label='ID Number')

# between dates

class DateRangeForm(forms.Form):
    from_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='From Date'
    )
    to_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='To Date'
    )
class add_book_master(forms.Form):
    book_name=forms.CharField(label='Book Name')
    date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date'
    }))

class master_data_form(forms.Form):
    id_number = forms.CharField(label='ID Number')

class searech_book_data(forms.Form):
    book_name=forms.CharField(label='Search Book Name')

class vendor_data(forms.Form):
    company_name=forms.CharField(label='Enter company Name')
    company_address=forms.CharField(label='Enter Address')
    gst=forms.CharField(label='Enter Gst Number')
    phone_number=forms.CharField(label='Enter Phone Number')
    city=forms.CharField(label='Enter City')
    state=forms.CharField(label='Enter State')
    pincode=forms.CharField(label='Enter Pincode')

class bill_generate_form(forms.Form):
    company_name=forms.CharField(label='Enter Company Name')
    billing_address=forms.CharField(label='Enter Bill Address')
    shiping_address=forms.CharField(label='Enter Shiping Address')
    eway_number=forms.IntegerField(label='Enter Eway Number')
    purchase_number=forms.CharField(label='Enter PO Number')
    purchase_date=forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date'
    }))


class search_unit_address(forms.Form):
    unit_name=forms.CharField(label='Enter Unit Name')


#################Form API#######################DATA########################################
# class searech_book_data(forms.Form):
#     SEARCH_CHOICES = [
#         ('book_name', 'Book Name'),
#         ('book_id_number', 'Book ID Number')
#     ]
    
#     search_by = forms.ChoiceField(choices=SEARCH_CHOICES, label='Search By')
#     search_term = forms.CharField(label='Enter Search Term')
# forms.py
from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('user', 'User'), ('admin', 'Admin')])

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

# from django import forms

# class LoginForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=100)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
