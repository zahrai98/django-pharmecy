from django import forms
from .models import Comment


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =('body',)
        widgets = {
            'body' : forms.Textarea(attrs={'class':'form-content'},)
        }
        labels = {
            'body' : 'متن'
        }
        error_messages ={
            'body':{
                'required':'این فیلد اجباری است',
            }
        }
        help_text ={
            'body': 'حداکثر 500 کاراکتر'
        }


class AddReplytForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =('body',)
