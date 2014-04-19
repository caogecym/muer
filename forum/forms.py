import re
from datetime import date
from django import forms
from forum.models import *
from django.utils.translation import ugettext as _

class TitleField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(TitleField, self).__init__(*args, **kwargs)
        self.required = True
        self.max_length = 255
        self.label  = _('title')
        self.help_text = _('please enter a descriptive title for your question')
        self.initial = ''

    def clean(self, value):
        if len(value) < 5:
            raise forms.ValidationError(_('title must be at least 5 characters'))

        return value

class ContentField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(ContentField, self).__init__(*args, **kwargs)
        self.required = True
        self.max_length = 4096
        self.label  = _('content')
        self.help_text = _('please enter a descriptive title for your question')
        self.initial = ''

class TagNamesField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(TagNamesField, self).__init__(*args, **kwargs)
        self.required = True
        self.max_length = 255
        self.label  = _('tags')
        self.help_text = _('Tags are short keywords, with no spaces within. Up to five tags can be used.')
        self.initial = ''

        def clean(self, value):
                value = super(TagNamesField, self).clean(value)
                data = value.strip()
                if len(data) < 1:
                        raise forms.ValidationError(_('tags are required'))
                list = data.split(' ')
                list_temp = []
                if len(list) > 5:
                        raise forms.ValidationError(_('please use 5 tags or less'))
                for tag in list:
                        if len(tag) > 20:
                                raise forms.ValidationError(_('tags must be shorter than 20 characters'))
                        #take tag regex from settings
                        tagname_re = re.compile(r'[a-z0-9]+')
                        if not tagname_re.match(tag):
                                raise forms.ValidationError(_('please use following characters in tags: letters \'a-z\', numbers, and characters \'    .-_#\''))
                        # only keep one same tag
                        if tag not in list_temp and len(tag.strip()) > 0:
                                list_temp.append(tag)
                return u' '.join(list_temp)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields=('title', 'content', 'tagnames')
