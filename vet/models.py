from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Diseases(models.Model):
    title = models.CharField(max_length=150, db_index=True, blank=False, null=False, verbose_name="Назва захворювання")
    feature = models.TextField(blank=True, verbose_name="Ознаки захворювання")
    treatment = models.TextField(blank=True, verbose_name="Рекомендації щодо лікуання")
    photo = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Фото', blank=True)

    # method create url for every category on link category upper every2 news
    def get_absolute_url(self):
        return reverse("properties_disease", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'Захворювання'
        verbose_name_plural = 'Захворювання'
        ordering = ['title']

    def __str__(self):
        return self.title


class PhotoImage(models.Model):
    """its helper class to add 2 photo for one diseases"""
    diseases = models.ForeignKey(Diseases, default=None, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Фото', blank=True)

    def __str__(self):
        return self.diseases.title


class CustomUser(AbstractUser):
    phone = models.CharField(null=True, blank=True, max_length=12, validators=[RegexValidator(r'^\d{3}-\d{3}-\d{4}$')],
                             verbose_name='Телефон')
    # email = models.EmailField(max_length=70, blank=False, unique=True, null=False, verbose_name='Емейл')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Адресса')
    user_photo = models.ImageField(upload_to='user_photo_images/%Y/%m/%d/', verbose_name='Фото', blank=True)
    position = models.CharField(max_length=150, blank=True, verbose_name="Посада")

    # str view information when print
    # return query set of titles
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'
        ordering = ['last_name']


class SendEmailModel(models.Model):
    client_name = models.CharField(max_length=150, blank=True, verbose_name="Ім'я", )
    client_email = models.EmailField(null=False, max_length=70, blank=False, verbose_name='E-mail', )
    content = models.TextField(blank=True, verbose_name="Текст повідомлення", )
    vet_member = models.ForeignKey(CustomUser, default=None, on_delete=models.CASCADE,
                                   null=False, blank=False, verbose_name="Ветеринарний лікар")

    class Meta:
        verbose_name = 'Записи на консультацію'
        verbose_name_plural = 'Записи на консультації'

    def __str__(self):
        return self.client_email


class Animal_breed(models.Model):
    breed = models.CharField(max_length=150, null=False, blank=False, verbose_name="Порода тварини")

    class Meta:
        verbose_name = 'Порода тварини'
        verbose_name_plural = 'Породи тварин'

    def __str__(self):
        return self.breed


class Animal(models.Model):
    CHOICES = (
        ('кішка', 'Кішка'),
        ('сука', 'Сука'),)
    animal_name = models.CharField(max_length=150, blank=False, verbose_name="Кличка тварини")
    animal_weight = models.FloatField(null=False, blank=False, verbose_name='Вага тварини')
    animal_age = models.FloatField(null=False, blank=False, verbose_name='Вік тварини')
    diseases = models.ForeignKey(Diseases, default=None, on_delete=models.CASCADE, verbose_name='Захворювання')
    bread = models.ForeignKey(Animal_breed, default=None, on_delete=models.CASCADE, verbose_name='Порода тварини')
    animal_owner = models.ForeignKey(CustomUser, default=None, on_delete=models.CASCADE,
                                     verbose_name="Господар тварини")
    kind_of_animal = models.CharField(max_length=150, choices=CHOICES, verbose_name="Вид тварини")

    class Meta:
        verbose_name = 'Тварина'
        verbose_name_plural = 'Тварини'
        ordering = ['animal_name']

    def __str__(self):
        return self.animal_name


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Титул')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публікації')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    author = models.ForeignKey(CustomUser, default=None, on_delete=models.CASCADE, verbose_name="Автор")

    """required fields: title, photo
    content (blank = True) - not required
    data fields are auto fill
    photo fill are not required while work/fill fields from terminal/console
    """

    # method create url for every news on button "Read more"
    def get_absolute_url(self):
        return reverse("view_news", kwargs={"pk": self.pk})

    # str view information when print
    # return query set of titles
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новина'
        verbose_name_plural = 'Новини'
        ordering = ['-created_at']
