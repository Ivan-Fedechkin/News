from datetime import datetime
from django.views.generic import TemplateView
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.models import Group
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Author, Category
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class PostList(ListView):
    model = Post
    ordering = 'time'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 4

class SearchPost(ListView):
    model = Post
    ordering = '-rating_post'
    template_name = 'search_news.html'
    context_object_name = 'search'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['New posts is coming soon'] = None
        return context

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def post(self, request, *args, **kwargs):
        post_mail = Post(author=Author.objects.get(user=self.request.user),
                         select_choices=request.POST.get('select_choices'),
                         heading_post=request.POST.get('heading_post'),
                         text_post=request.POST.get('text_post'))

        #if limitation_post(sender=Post, instance=post_mail, **kwargs) < 10000000:
        post_mail.save()
        post_mail.category.add(*request.POST.getlist('category'))
        #else:
            #print('Нельзя создавать больше 3х статей за день')

        return redirect('/')

    def form_valid(self, form):
        if self.request.path == '/news/articles/create':
            post = form.save(commit=False)
            post.select_choices = 'AR'
        else:
            post = form.save(commit=False)
            post.select_choices = 'NE'
        return super().form_valid(form)

class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = '/news/'

class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/news/')

@login_required
def subscribe(request, i):
    user_ = User.objects.get(username=request.user)
    if user_:
        cat1 = Category.objects.get(pk=i)
        post1 = user_
        cat1.subscribers.add(post1)
    return redirect('/news/')

@login_required
def unsubscribe(request, **kwargs):
    post = Post.objects.get(pk=kwargs['pk'])
    user = request.user
    for category in post.category.all():
        if user in category.subscribers.all():
            category.subscribers.remove(user)

    return redirect(request.META.get('HTTP_REFERER', '/'))



