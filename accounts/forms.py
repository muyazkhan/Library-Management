from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserAccount,GENDER_TYPE


class registaionForm(UserCreationForm):
    phone_no = forms.CharField(max_length=11)
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','phone_no','gender','password1', 'password2']
    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            phone_no = self.cleaned_data.get("phone_no")
            gender = self.cleaned_data.get("gender")

            UserAccount.objects.create(
                phone_no=phone_no,
                gender=gender,
                user=user,
                customer_id=1000 + user.id
            )
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({   
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })  
        

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
class UpdateForm(forms.ModelForm):
    phone_no = forms.CharField(max_length=11)
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            try:
                user_account = self.instance.user_account
            except:
                user_account = None

            if user_account:
                self.fields['phone_no'].initial = user_account.phone_no
                self.fields['gender'].initial = user_account.gender


    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            user_account, created = UserAccount.objects.get_or_create(user=user)
            user_account.phone_no = self.cleaned_data.get("phone_no")
            user_account.gender = self.cleaned_data.get("gender")
            user_account.save()

        return user