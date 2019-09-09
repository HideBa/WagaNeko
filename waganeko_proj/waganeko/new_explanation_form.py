from django.forms import Form, ModelForm, HiddenInput
from waganeko.models import Explanation, Summary
from django import forms

class NewExplanationForm(ModelForm):
    class Meta:
        model = Explanation
        fields = ['tweet']

        labels = {'tweet': '投稿内容'}
    # post_text = forms.CharField(widget=forms.Textarea)

# class NewExplanationForm(forms.Form):
#     class Meta:
#         model = Explanation
#         fields = [
#             'post_text',
#         ]

#         label = {
#             'post_text':'投稿',
#         }
