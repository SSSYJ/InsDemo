from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.forms import UserCreationForm
from Insta.forms import CustomUserCreationForm

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Like, InsUser, UserConnection, Comment
from annoying.decorators import ajax_request


class HelloWorld(TemplateView): # HelloWorld is-a TempateView
    template_name = 'test.html'


class PostsView(ListView):
    model = Post
    template_name = 'index.html'
    
    # def get_queryset(self):
    #     current_user = self.request.user
    #     following = set()
    #     for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
    #         following.add(conn.following)
    #     return Post.objects.filter(author__in=following)

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = '__all__'
    login_url = 'login'

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy("posts")

class SignUp(CreateView):
    template_name = 'signup.html'
    success_url = reverse_lazy("login")
    form_class = CustomUserCreationForm

class UserProfile(LoginRequiredMixin, DetailView):
    model = InsUser
    template_name = 'user_profile.html'
    login_url = 'login'

class EditProfile(LoginRequiredMixin, UpdateView):
    model = InsUser
    template_name = 'profile_update.html'
    fields = ['username', 'profile_pic']

@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk = post_pk)
    try:
        like = Like(post = post, user = request.user)
        like.save() #if it is already existed, due to unique_together, it will throw exceptions  
        result = 1 
    except Exception:
        like = Like.objects.get(post = post, user = request.user)
        like.delete() #since it is existed,  click the heart again will delete the like
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }

@ajax_request
def addComment(request):
    content = request.POST.get('comment_text')
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk = post_pk)
    commenter_info = {}

    try:
        comment = Comment(post = post, creator = request.user, content = content)
        comment.save()
        commenter_info = {
            'username': request.user.username,
            'comment_text': content
        }
    
        result = 1 
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }

@ajax_request
def toggleFollow(request):
    current_user = InsUser.objects.get(pk=request.user.pk)
    follow_user_pk = request.POST.get('follow_user_pk')
    follow_user = InsUser.objects.get(pk=follow_user_pk)

    try:
        if current_user != follow_user:
            if request.POST.get('type') == 'follow':
                connection = UserConnection(creator=current_user, following=follow_user)
                connection.save()
            elif request.POST.get('type') == 'unfollow':
                UserConnection.objects.filter(creator=current_user, following=follow_user).delete()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'type': request.POST.get('type'),
        'follow_user_pk': follow_user_pk
    }
