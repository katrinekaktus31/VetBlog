from django.urls import include, path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', General.as_view(), name='general'),
    path('blog/', NewsBlog.as_view(), name="blog"),
    path('create_news/', CreateNews.as_view(), name='create_news'),
    path('view_news/<int:pk>/', ViewNews.as_view(model=News), name='view_news'),
    path('diseases/', DiseasesList.as_view(), name='diseases_list'),
    path('properties_disease/<int:pk>/', ProportiesDiseases.as_view(model=Diseases), name='properties_disease'),
    path('send_mail/', SendEmailTo.as_view(), name='send_mail'),
    path('vet_members/', VetMembersList.as_view(), name='vet_members_list'),
    path('registration/', registration, name='registration'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout')

]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

