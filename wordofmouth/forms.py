from django import forms
from .models import Comment
from .models import Recipe

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')

        widgets = {'name': forms.TextInput(attrs={'class':'form-control'}),
                   'body': forms.Textarea(attrs={'class': 'form-control'})
                   }
class EditForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'ingredients', 'instructions')