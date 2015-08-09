from django.forms import ModelForm, ValidationError, Textarea
from gnsite.models import Post
from django.utils.translation import ugettext as _

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'link', 'desc']
        widgets = {
            'desc': Textarea(attrs={'cols': 60, 'rows': 6}),
        }

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        link = cleaned_data.get('link')
        if link == '': link = None
        desc = cleaned_data.get('desc')
        if desc == '': desc = None
        if not link and not desc:
            raise ValidationError(_("Please try again"))
        if link and desc:
            raise ValidationError(_("Please try again"))

class CommentForm(ModelForm):
    class Meta:
        model = Post
        fields = ['desc']
        widgets = {
            'desc': Textarea(attrs={'cols': 60, 'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['desc'].required = True

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        desc = cleaned_data.get('desc')
        if not desc:
            raise ValidationError(_("Please try again"))

