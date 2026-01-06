from django import forms
from .models import Event, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group, Permission


class StyledFormMixin:
    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field in self.fields.values():
            field.widget.attrs.update({'class': self.default_classes})


# Event Form
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__' 
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded px-2 py-1 w-full'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'border rounded px-2 py-1 w-full'}),
            'title': forms.TextInput(attrs={'class': 'border rounded px-2 py-1 w-full'}),
            'description': forms.Textarea(attrs={'class': 'border rounded px-2 py-1 w-full', 'rows': 4}),
            
            'image': forms.ClearableFileInput(attrs={'class': 'border rounded px-2 py-1 w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.DateInput, forms.TimeInput, forms.ClearableFileInput)):
                field.widget.attrs.update({'class': 'border rounded px-2 py-1 w-full'})


# Category Form
class CategoryForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()


# User Registration Form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]



class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']
