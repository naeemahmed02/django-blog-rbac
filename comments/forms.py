from django import forms
from comments.models import Comments

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4,
            }),
        }
