import os

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.template.loader import render_to_string

from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import Advertsement, Replies, News
from .forms import AdvertsementForm, RepliesForm, NewsForm

from typing import Any, Dict
from sign.models import MyUser

from .filters import RepliesFilter

def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'message_boards/page.html', context={'var': os.environ})


class AdvertsementListView(ListView):
    '''Вьюха отображает все объявления'''
    model = Advertsement
    template_name = 'message_boards/advertsements_list_all.html'
    context_object_name = 'advertsements'
    paginate_by = 3
    # добавляем форм класс, чтобы получать доступ к форме через метод POST

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'adversements': Advertsement.objects.all(),

        }


class AdvertsementsUserView(LoginRequiredMixin, ListView):
    '''Вьюха отображает все объявления текущего юзера'''
    model = Advertsement
    template_name = 'message_boards/advertsements_list_user.html'
    context_object_name = 'advertsements'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        user_id = MyUser.objects.get(username=self.request.user).id
        return {
            **super().get_context_data(*args, **kwargs),
            'advertsements': Advertsement.objects.filter(user_id=user_id)
        }


class AdvertsementCreateView(LoginRequiredMixin, CreateView):
    '''Вьюха создания нового объявления'''
    model = Advertsement
    form_class = AdvertsementForm
    template_name = 'message_boards/advertsement_create.html'
    # success_url = '/news/'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> "HttpResponse":
        form = self.form_class(request.POST)
        if form.is_valid():
            advertsement = Advertsement(
                title=request.POST['title'],
                body=request.POST['body'],
                category=request.POST['category'],
                user_id=MyUser.objects.get(username=request.user.username).id
            )
            advertsement.save()
        return redirect('advertsement_list')


class AdvertsementUpdateView(LoginRequiredMixin, UpdateView):
    '''Вьюха редактировантя объявления'''
    template_name = 'message_boards/advertsement_create.html'
    form_class = AdvertsementForm

    # метод get_object мы используем вместо queryset,
    # чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Advertsement.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context


class AdvertsementDetailView(DetailView):
    '''Вьюха детелизации объявления'''
    model = Advertsement
    template_name = 'message_boards/advertsement_detail.html'
    context_object_name = 'advertsement'
    success_url = 'adversement/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Advertsement.objects.get(pk=id)


class AdvertsementDeleteView(DeleteView):
    template_name = 'message_boards/advertsement_delete.html'
    queryset = Advertsement.objects.all()
    success_url = '/advertsement/'


class RepliesAdvertsementCreate(LoginRequiredMixin, CreateView):
    '''Вьюха отображает создание отклика к объявления'''
    template_name = 'message_boards/replies_create.html'
    form_class = RepliesForm
    # context_object_name = 'replies'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Advertsement.objects.get(pk=id)

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'advertsement': self.get_object()
        }

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            replies = Replies(
                body=request.POST['body'],
                advertsement_id=self.get_object().id,
                user_id=self.request.user.id
            )
            replies.save()
        return redirect('advertsement_list')


class RepliesUserListView(LoginRequiredMixin, ListView):
    model = Replies
    template_name = 'message_boards/replies_list_user.html'
    context_object_name = 'replies'
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        user_id = MyUser.objects.get(username=self.request.user).id
        advertsement_ids = Advertsement.objects.filter(user_id=user_id)
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = RepliesFilter(self.request.GET, queryset=self.get_queryset())
        context['replies'] = Replies.objects.filter(advertsement_id__in=advertsement_ids)
        return context


class ReplyUserDetail(DetailView):
    model = Replies
    template_name = 'message_boards/reply_detail.html'
    context_object_name = 'reply'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Replies.objects.get(pk=id)


class ReplyDeleteView(DeleteView):
    template_name = 'message_boards/reply_delete.html'
    queryset = Replies.objects.all()
    success_url = '/advertsement/user_replies/'


def reply_accept(request, *args, **kwargs):
    reply = Replies.objects.get(id=kwargs['pk'])
    user_reply_id = reply.user_id
    user = MyUser.objects.get(id=user_reply_id)

    html_content = render_to_string(
        'message_boards/email_response_reply.html',
        {
            'user': user
        }
    )
    msg = EmailMultiAlternatives(
        subject={reply.body},
        body=f"Ответ на отклик",
        from_email='Lafen55@yandex.ru',
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponse('<h1>Готово!</h1>')


class NewsCreate(CreateView):
    model = News
    form_class = NewsForm
    template_name = 'message_boards/news_create.html'

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> "HttpResponse":
        form = self.form_class(request.POST)
        if form.is_valid():
            news = News(
                title = request.POST['title'],
                body = request.POST['body']
            )
            news.save()
        return redirect('advertsement_list')  #FIXME
