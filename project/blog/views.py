from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Category, Article, Comment, Like, Profile
from .forms import ArticleForm, LoginForm, RegistrationForm, CommentForm, EditUserForm, EditProfileForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login, logout
from django.contrib import messages

"""Create your views here."""


# def index(request):
#    articles = Article.objects.all()
#
#    context = {
#       'title': 'PROWEB-БЛОГ - Главная страница',
#       'articles': articles
#    }
#    return render(request, 'blog/index.html', context)


class ArticleListView(ListView):  # article_list.html - если не указать
    model = Article
    template_name = 'blog/index.html'  # иначе адрес article_list.html
    context_object_name = 'articles'  # иначе имя будет objects
    extra_context = {
        'title': 'Главная страница'
    }

    # Для сортировки
    def get_queryset(self):
        articles = Article.objects.all()
        sort_field = self.request.GET.get('sort')
        if sort_field:
            articles = articles.order_by(sort_field)
        return articles

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        articles = Article.objects.all()
        articles = articles.order_by('created_at')
        context['slider'] = articles[:5]
        return context


# def articles_by_category(request, category_id):
#    articles = Article.objects.filter(category_id=category_id)
#    category = Category.objects.get(pk=category_id)
#    context = {
#       'title': f'Категория: {category.title}',
#       'articles': articles
#    }
#    return render(request, 'blog/index.html', context)


class ArticleByCategory(ArticleListView):
    # переделать стандартный вывод статей (ВСЕХ)
    def get_queryset(self):
        articles = Article.objects.filter(category_id=self.kwargs['category_id'])
        sort_field = self.request.GET.get('sort')
        if sort_field:
            articles = articles.order_by(sort_field)
        return articles

    # Динамическая отправка контекста
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()  # Все что было и так сохранить
        category = Category.objects.get(pk=self.kwargs['category_id'])
        context['title'] = f'Категория: {category.title}'
        return context


# def article_detail(request, article_id):
#    article = Article.objects.get(pk=article_id)
#    context = {
#       'article': article,
#       'title': f'Статья: {article.title}'
#    }
#    return render(request, 'blog/article_detail.html', context)


class ArticleDetailView(DetailView):  # article_detail.html - такой и должен быть адрес
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article = Article.objects.get(pk=self.kwargs['pk'])
        article.views += 1
        article.save()
        user = self.request.user

        # если только лайки
        # if not Like.objects.filter(user=user, article=article).exists():
        #    context['like'] = False
        # else:
        #    like = Like.objects.get(user=user, article=article)
        #    context['like'] = like.like # True или False

        if user.is_authenticated:
            mark, created = Like.objects.get_or_create(user=user, article=article)
            if created:
                context['like'] = False
                context['dislike'] = False
            else:
                context['like'] = mark.like
                context['dislike'] = mark.dislike
        else:
            context['like'] = False
            context['dislike'] = False

        context['title'] = f'Статья на тему: {article.title}'
        """Если пользователь авторизован вернуть ему форму"""
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(article_id=self.kwargs['pk'])
        return context


# def add_article(request):
#    if request.method == 'POST':
#       form = ArticleForm(request.POST, request.FILES)
#       if form.is_valid():
#          title = form.cleaned_data['title']
#          article = Article.objects.create(**form.cleaned_data)
#          article.save()
#          return redirect('article_detail', article.pk)
#    else:
#       form = ArticleForm
#
#    context = {
#       'form': form,
#       'title': 'Добавить статью'
#    }
#    return render(request, 'blog/article_form.html', context)


class NewArticle(CreateView):  # GET POST не надо делать, класс сделает всё сам
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    extra_context = {
        'title': 'Добавить статью'
    }


class ArticleUpdate(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'


class ArticleDelete(DeleteView):
    model = Article
    success_url = reverse_lazy('index')  # куда перейти после удаления
    context_object_name = 'article'


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в аккаунт!')
                return redirect('index')
            else:
                messages.error(request, 'Не верные логин/пароль')
                return redirect('login')
        else:
            return redirect('login')
    else:
        form = LoginForm()
        context = {
            'title': 'Авторизация пользователя',
            'form': form
        }
        return render(request, 'blog/user_login.html', context)


def user_logout(request):
    logout(request)
    messages.warning(request, 'Вы вышли из аккаунта')
    return redirect('index')


def about_the_site(request):
    context = {
        'title': 'О сайте'
    }
    return render(request, 'blog/about_site.html', context)


def about_the_developer(request):
    context = {
        'title': 'О разработчике'
    }
    return render(request, 'blog/about_developer.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            messages.success(request, 'Регистрация прошла успешно. Войдите в аккаунт.')
            return redirect('login')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('register')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
        'title': 'Регистрация Пользователя'
    }
    return render(request, 'blog/register.html', context)


def save_comment(request, pk):
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = Article.objects.get(pk=pk)
        comment.user = request.user
        comment.save()
        messages.success(request, 'Ваш комментарий успешно сохранён!')
        return redirect('article_detail', pk)


"""Оформить красиво комментарии
Вывод ошибок при регистрации
Лайки и Дизлайки
Отображение в админке комментариев"""


# если только лайки
# def add_or_delete_like(request, article_id):
#    user = request.user
#    article = Article.objects.get(pk=article_id)
#    like, created = Like.objects.get_or_create(user=user, article=article)
#    if created:
#       like.like = True
#       like.save()
#    else:
#       like.like = False if like.like else True # False если был True иначе True
#       like.save()
#    return redirect('article_detail', article.pk)


def add_or_delete_mark(request, article_id, action):
    user = request.user
    if user.is_authenticated:
        article = Article.objects.get(pk=article_id)
        mark, created = Like.objects.get_or_create(user=user, article=article)
        if action == 'addlike':
            mark.like = True
            mark.dislike = False
        elif action == 'adddislike':
            mark.like = False
            mark.dislike = True
        elif action == 'deletelike':
            mark.like = False
        elif action == 'deletedislike':
            mark.dislike = False
        mark.save()
        return redirect('article_detail', article.pk)
    else:
        return redirect('login')


"""
1. Поисковик - ✔
2. фильтр статей на главной - ✔
3. уникальные просмотры - ✔
4. страница аккаунта - 
слайдер последних статей - видео
удаление своих комментариев - видео
"""


class SearchResults(ArticleListView):
    def get_queryset(self):
        word = self.request.GET.get('q')
        articles = Article.objects.filter(title__icontains=word)
        return articles


def profile(request):
    user_profile = Profile.objects.get(user=request.user)
    context = {
        'profile': user_profile
    }
    return render(request, 'blog/profile.html', context)


def userEditView(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваши данные успешно изменены')
            return redirect(to='profile')
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user)

    return render(request, 'blog/edit_account.html', {'form': user_form, 'form2': profile_form})


def delete_comment(request, comment_id, article_id):
    comment = Comment.objects.get(pk=comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect('article_detail', article_id)
