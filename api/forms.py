from django import forms
from .models import users_collection

Branch = {
    ('hyderabad', 'hyderabad'), 
    ('bangalore', 'bangalore'),
    ('chennai', 'chennai'), 
    ('mumbai', 'mumbai'), 
    ('tirupati', 'tirupati'),
    ('vizag', 'vizag'),
    ('pune', 'pune'), 
    ('delhi', 'delhi'), 
    ('kochi', 'kochi'),
    ('Venkatagiri', 'Venkatagiri') 
    }

class RegisterForm(forms.Form): 
    username = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})) 
    email = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})) 
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})) 
    homeBranch = forms.ChoiceField(choices=Branch, widget=forms.Select(attrs={'class': 'form-control'}))

class AdminRegisterForm(forms.Form): 
    username = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})) 
    email = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})) 
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})) 



class LoginForm(forms.Form): 
    email = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})) 
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})) 


paymentMethods = {
    
    ('IMPS', 'IMPS'),
    ('NEFT', 'NEFT'),
    ('RTGS', 'RTGS'),
    ('UPI', 'UPI')
    
    }

class TransferForm(forms.Form): 
    senderId = forms.CharField(max_length = 200, widget=forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Sender Id'})) 
    senderName = forms.CharField(widget = forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'senderName'})) 
    remarks = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'remarks'}))
    receiverId = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'receiverId'}))
    receiverIFSC = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'receiverIFSC'}))
    amount = forms.IntegerField(widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'amount'}))
    paymentMethod = forms.ChoiceField(choices= paymentMethods, widget = forms.Select(attrs={'class': 'form-control', 'placeholder': 'paymentMethod'}))



class DepositForm(forms.Form): 
    depositName = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'depositName'})) 
    customerId = forms.CharField(widget = forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'customerId'}))
    customerName = forms.CharField(widget = forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'customerName'}))
    nomineeName = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nomineeName'}))
    nomineeAge = forms.IntegerField(widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'nomineeAge'}))
    duration = forms.IntegerField(widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'duration'}))
    amount = forms.IntegerField(widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'amount'}))
    

loan_types = {
    ('vehicle-loan', 'vehicle-loan'),
    ('home-loan', 'home-loan'),
    ('personal-loan', 'personal-loan'),
    ('education-loan', 'education-loan'),
    ('business-loan', 'business-loan')   
}

class LoanForm(forms.Form): 
    loanType = forms.ChoiceField(choices=loan_types, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'loanType'}))
    customerId = forms.CharField(widget = forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'customerId'}))
    customerName = forms.CharField(widget = forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'customerName'}))
    nomineeName = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nomineeName'}))
    nomineeAge = forms.IntegerField(widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'nomineeAge'}))
    duration = forms.IntegerField(widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'duration'}))
    loanAmount = forms.IntegerField(widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'amount'}))
    