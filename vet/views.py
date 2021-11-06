from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin

from .forms import CustomUserCreationForm, AnimalCreationForm, UserLoginForm, NewsForm, SendEmailForm
from .models import Diseases, CustomUser, News, SendEmailModel
from .service import send_to_vet_member, send_to_user


# Create your views here.

def registration(request):
    """ funс that register new users with their pets. create Animal and User"""
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        animal_form = AnimalCreationForm(request.POST)

        if user_form.is_valid() and animal_form.is_valid():
            user = user_form.save()
            animal = animal_form.save(commit=False)
            animal.animal_owner = user
            animal.save()
            login(request, user)
            messages.success(request, 'Ви успішно зареєстровані!')
            return redirect('properties_disease', pk=animal.diseases.pk)
        else:
            messages.error(request, 'Помилка реестрації!')
    else:
        user_form = CustomUserCreationForm()
        animal_form = AnimalCreationForm()
    context = {
        'user_form': user_form,
        'animal_form': animal_form,
    }
    return render(request, 'vet/registration.html', context)


def user_login(request, ):
    """ func that login all users from CustonUser """
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next = request.GET.get('next')
            if next:
                return redirect(next)
            else:
                return redirect('diseases_list')
    else:
        form = UserLoginForm()
    return render(request, 'vet/login.html', {'form': form})


def user_logout(request):
    """logout all users"""
    logout(request)
    return redirect('login')


class General(ListView):
    """ general page view """
    model = CustomUser
    template_name = 'vet/general.html'
    context_object_name = 'users'

    def get_queryset(self):
        return CustomUser.objects.filter(groups__name='Staff')


class NewsBlog(ListView):
    """ func that view all news model """
    model = News
    template_name = 'vet/blog.html'
    context_object_name = 'news'

    def get_queryset(self):
        return News.objects.filter(author_id__groups__name='Staff').select_related('author')


class CreateNews(PermissionRequiredMixin, CreateView):
    """create news form for staff users """
    permission_required = ('vet.add_news', 'vet.change_news', 'vet.delete_news')
    form_class = NewsForm
    template_name = 'vet/create_news.html'



class ViewNews(DetailView):
    """ func that view news details for all users"""
    model = News
    template_name = 'vet/view_news.html'
    context_object_name = 'news_item'


class DiseasesList(ListView):
    """ func that view all diseases """
    model = Diseases
    template_name = 'vet/disease_list.html'
    context_object_name = 'diseases'
    # category queryset for greedy select from model
    # queryset = Diseases.objects.select_related('category')


class ProportiesDiseases(DetailView):
    """ func that view detail about diseases"""
    model = Diseases
    template_name = 'vet/properties_disease.html'
    context_object_name = 'disease'
    # category queryset for greedy select from model
    # queryset = Diseases.objects.select_related('category')


class VetMembersList(ListView):
    """ func that view all users, who are staff """
    model = CustomUser
    template_name = 'vet/vet_members.html'
    context_object_name = 'users'

    def get_queryset(self):
        return CustomUser.objects.filter(groups__name='Staff')




class SendEmailTo(CreateView):
    form_class = SendEmailForm
    success_url = '/'
    template_name = 'vet/send_mail.html'

    def get_queryset(self):
        return SendEmailModel.objects.filter(vet_member_id__groups__name='Staff')

    def form_valid(self, form):
        form.save()
        send_to_vet_member(form.instance.client_email, form.instance.content,
                                             form.instance.client_name)
        send_to_user(form.instance.client_email)
        return super().form_valid(form)

