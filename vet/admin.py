from django.contrib import admin
from .models import Diseases, PhotoImage, News, Animal, CustomUser, Animal_breed, SendEmailModel
# Kind_of_Dog, Kind_of_Cat, Dog_breed, Cat_breed
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    creation_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Додаткова інформація',
            {
                'fields': (
                    'phone',
                    'address',
                    'user_photo',
                    'position',
                )
            }
        )
    )


admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(SendEmailModel)
class SendEmailModelAdmin(admin.ModelAdmin):
    pass

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass

@admin.register(Animal_breed)
class Animal_breedAdmin(admin.ModelAdmin):
    pass

# @admin.register(Dog_breed)
# class Dog_breedAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(Cat_breed)
# class Cat_breedAdmin(admin.ModelAdmin):
#     pass


class PhotoImageAdmin(admin.StackedInline):
    model = PhotoImage


@admin.register(Diseases)
class DiseasesAdmin(admin.ModelAdmin):
    inlines = [PhotoImageAdmin]

    class Meta:
        model = Diseases


@admin.register(PhotoImage)
class PhotoImageAdmin(admin.ModelAdmin):
    pass

#
# class AnimalAdmin(admin.StackedInline):
#     model = Animal


# @admin.register(Kind_of_Cat)
# class Kind_of_CatAdmin(admin.ModelAdmin):
#     inlines = [AnimalAdmin]
#
#     class Meta:
#         model = Kind_of_Cat
#
#
# @admin.register(Kind_of_Dog)
# class Kind_of_DogAdmin(admin.ModelAdmin):
#     inlines = [AnimalAdmin]
#
#     class Meta:
#         model = Kind_of_Dog


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    pass
