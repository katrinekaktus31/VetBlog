from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import re
from django.core.exceptions import ValidationError

from .models import CustomUser, Animal, News, SendEmailModel


class SendEmailForm(forms.ModelForm):
    client_name = forms.CharField(max_length=150, label="Ім'я", help_text="Вкажіть своє ім'я",
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    client_email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={"class": "form-control"}))
    content = forms.CharField(label="Текст повідомлення",
                              help_text='Короткий опис причини звернення до ветеринарного лікаря', required=False,
                              widget=forms.Textarea(attrs={
                                  "class": "form-control",
                                  "rows": 5
                              }))
    vet_member = forms.ModelChoiceField(queryset=CustomUser.objects.filter(groups__name='Staff'),
                                        label="Ветеринарний лікар", empty_label="Оберіть ветеринарного лікаря",
                                        widget=forms.Select(attrs={"class": "form-control"}))

    class Meta:
        model = SendEmailModel
        fields = ['client_name', 'client_email', 'content', 'vet_member']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Ім`я користувача / Login',
                               widget=forms.TextInput(attrs={"class": "form-control", }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}))


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="Ім`я користувача / Login", max_length=150, help_text="Максимум 150 символів",
                               widget=forms.TextInput(
                                   attrs={"class": "form-control", }))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label='Підтвердження паролю',
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="Ім'я", max_length=150, widget=forms.TextInput(
        attrs={"class": "form-control", }))
    last_name = forms.CharField(label="Прізвище", max_length=150,
                                widget=forms.TextInput(attrs={"class": "form-control", }))
    phone = forms.IntegerField(label="Телефон", required=False, help_text="* За бажанням",
                               widget=forms.TextInput(attrs={"class": "form-control", }))
    address = forms.CharField(label="Адреса", max_length=150, required=False, help_text="* За бажанням",
                              widget=forms.TextInput(attrs={"class": "form-control", }))
    user_photo = forms.FileField(label="Фото", required=False, help_text="* За бажанням",
                                 widget=forms.FileInput(attrs={"class": "form-control", })),
    position = forms.CharField(label="Посада", max_length=150, required=False,
                               widget=forms.TextInput(attrs={"class": "form-control", }))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name',
                  'phone', 'address', 'user_photo', 'position']


class AnimalCreationForm(forms.ModelForm):
    # animal_weight = forms.FloatField(required=True, min_value=0,
    #                                   widget=forms.NumberInput(attrs={"class": "form-control", 'step': '0.1'}))
    # animal_age = forms.FloatField(required=True, min_value=0,
    #                                   widget=forms.NumberInput(attrs={"class": "form-control", 'step': '0.1'}))

    def __init__(self, *args, **kwargs):
        """ add empty_label to Select widget """
        super().__init__(*args, **kwargs)
        self.fields["diseases"].empty_label = 'Оберіть хворобу'
        self.fields["bread"].empty_label = "Оберіть породу"
        self.fields["kind_of_animal"].empty_label = "Оберіть вид тварини"

    class Meta:
        model = Animal
        exclude = ('animal_owner',)
        fields = ['animal_name', 'animal_weight', 'animal_age', 'kind_of_animal', 'bread', 'diseases', ]
        widgets = {
            'animal_name': forms.TextInput(attrs={"class": "form-control"}),
            'animal_weight': forms.NumberInput(attrs={"class": "form-control", 'step': '0.1'}),
            'animal_age': forms.NumberInput(attrs={"class": "form-control", 'step': '0.1'}),
            'diseases': forms.Select(attrs={"class": "form-control"}),
            'bread': forms.Select(attrs={"class": "form-control"}),
            'kind_of_animal': forms.Select(attrs={"class": "form-control"})
        }


class NewsForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_staff=True),
                                    label="Автор", empty_label="Оберіть автора",
                                    widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        """ add empty_label to Select widget """
        super().__init__(*args, **kwargs)
        self.fields["author"].empty_label = "Оберіть автора"

    class Meta:
        model = News
        fields = ['title', 'content', 'photo', 'author']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            'photo': forms.FileInput(attrs={"class": "form-control", "enctype": "multipart/form-data"}),
        }

    def clean_title(self):
        """fun validate cleaned date from form. checks if the title starts with a number """
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError("Назва не повинна починатись з цифри")
        return title

    def clean_photo(self):
        file = self.cleaned_data['photo']
        if file:
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Image file is too large ( > 10mb ).")
        return file
        # if file:
        #     if file._size > 10 * 1024 * 1024:
        #         raise forms.ValidationError("Image file is too large ( > 10mb ).")
        #     return file
        # else:
        #     raise forms.ValidationError("Could not read the uploaded file.")
