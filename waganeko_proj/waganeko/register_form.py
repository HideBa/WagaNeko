from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from waganeko.models import GENDER_LIST, Profile

# from iekari.models import GENDER_LIST, Profile

class RegisterForm(UserCreationForm):
    age = forms.IntegerField(required=True)
    email = forms.EmailField(required=True)
    # household_num = forms.IntegerField(required=True)
    gender = forms.ChoiceField(choices=GENDER_LIST, required=True)
    belong = forms.CharField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','age','gender','belong']
        labels = {
            'username': 'ユーザー名',
            'email':'Email Adress',
            'password1': 'パスワード',
            'password2': 'パスワード確認',
            'age': '年齢',
            'gender': '性別',
            'belong': '所属',
        }

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError('Cannot create User and Profile without database save')

        user = super().save()

        try:
            max_id = Profile.objects.latest('id').id
        except ObjectDoesNotExist:
            max_id = 'U00000'

        prof_id = 'U'+(str(int(max_id[1:])+1).zfill(5))

        age = self.cleaned_data['age']
        gender = self.cleaned_data['gender']
        email = self.cleaned_data['email']
        belong = self.cleaned_data['belong']
        # household_num = self.cleaned_data['household_num']

        profile = Profile(id=prof_id,age=age,gender=gender, user_id=user.id, email = email, belong=belong)
        profile.save()

        return user
