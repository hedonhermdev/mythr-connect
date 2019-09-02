from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import UserRegistrationForm, UserLoginForm, CommentForm, NewPostForm, ProfileEditForm
from .models import Post, Comment


#       User and profile related views.

@login_required(login_url='/blog/accounts/login')
def user_profile_view(request, id):
    user = get_object_or_404(User, id=id)

    # Get the users details.
    context = {
        'user': user,
        'username': user.username,
        'name': f'{user.profile.first_name} {user.profile.last_name}',
        'about': user.profile.about,
        'birthdate': f'{user.profile.birthdate.strftime("%d-%m-%y")}',
        'num_followers': len(user.profile.followers.all()),
        'num_following': len(user.profile.follows.all()),
    }

    # Get the users posts.
    try:
        posts = user.posts.all()
    except Post.DoesNotExist:
        posts = []
    context.update({'posts': posts})
    return render(request, 'profiledetail.html', context=context)


@login_required(login_url='/blog/accounts/login')
def profile_edit_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            birthdate = form.cleaned_data['birthdate']
            about = form.cleaned_data['about']

            user.profile.first_name = first_name
            user.profile.last_name = last_name
            user.profile.birthdate = birthdate
            user.profile.about = about
            user.save()
            return redirect('blog-accounts-profile', id=user.id)
    else:
        form = ProfileEditForm({'first_name': user.profile.first_name,
                                'last_name': user.profile.last_name,
                                'birthdate': user.profile.birthdate,
                                'about': user.profile.about})
    return render(request, 'profileedit.html', context={'title': 'Edit Profile', 'form': form})


def register_view(request):
    if request.user.is_authenticated():
        return redirect(request, 'blog-home')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # User
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            # Profile
            user.profile.first_name = form.cleaned_data['first_name']
            user.profile.last_name = form.cleaned_data['last_name']
            user.profile.birthdate = form.cleaned_data['birthdate']
            user.profile.save()
            user.refresh_from_db()
            # Login
            user = authenticate(username=username, password=password)
            login(request, user)
            # Every user follows themself :)
            user.profile.follows.add(user.profile)
            return redirect('blog-home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', context={'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('blog-home')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog-home')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', context={'form': form})


def logout_view(request):
    logout(request)
    return redirect('blog-home')

#       Follow/unfollow views
@login_required(login_url='/blog/accounts/login/')
def user_follow_view(request, id):
    user_to_follow = get_object_or_404(User, id=id)
    follower = request.user
    if follower.profile not in user_to_follow.profile.followers.all():
        user_to_follow.profile.followers.add(follower.profile)
        user_to_follow.save()
    return redirect('blog-accounts-profile', id=id)


@login_required(login_url='/blog/accounts/login/')
def user_unfollow_view(request, id):
    user_to_unfollow = get_object_or_404(User, id=id)
    unfollower = request.user
    if unfollower.profile in user_to_unfollow.profile.followers.all():
        user_to_unfollow.profile.followers.remove(unfollower.profile)
        user_to_unfollow.save()
    return redirect('blog-accounts-profile', id=id)


#       Posts and comments related views.

@login_required(login_url='/blog/accounts/login/')
def post_detail_view(request, id):
    post = get_object_or_404(Post, id=id)
    context = {
        'post': post,
        'title': post.title,
        'content': post.content,
        'author': post.author,
        'date_posted': post.date_posted,
        'comments': post.comment_set.all(),
        'num_comments': post.comment_set.count()
    }
    return render(request, 'postdetail.html', context=context)


@login_required(login_url='/blog/accounts/login/')
def new_post_view(request):
    user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            post = Post.objects.create(title=title, content=content, author=user)
            return redirect('blog-post-detail', id=post.id)
    else:
        form = NewPostForm()
    return render(request, 'newpost.html', {'form': form})


@login_required(login_url='/blog/accounts/login/')
def new_comment_view(request, id):
    user = request.user
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(content=form.cleaned_data['content'], author=user, post=post)
            comment.save()
            return redirect('blog-post-detail', id=post.id)
    else:
        form = CommentForm()
    return render(request, 'newcomment.html', context={'form': form})


def post_edit_view(request, id):
    post = get_object_or_404(Post, id=id)

    if post.author == request.user:
        if request.method == 'POST':
            form = NewPostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                post.title = title
                post.content = content
                post.save()
                return redirect('blog-post-detail', id=id)
        else:
            form = NewPostForm({'title': post.title, 'content': post.content})
        return render(request, 'postedit.html', context={'title': 'Edit Post', 'form': form})


def post_delete_view(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user == post.author:
        if request.method == 'POST':
            post.delete()
            return redirect('blog-home')
    else:
        return redirect('blog-home')
    return render(request, 'postdelete.html', {'post': post})


#       Homepage and feedpage.

@login_required(login_url='/blog/accounts/login/')
def home(request):
    user = request.user
    title = 'Home Page'
    posts = list(Post.objects.all())
    context = {
        'user': user,
        'title': title,
        'posts': posts
    }
    return render(request, 'home.html', context=context)


@login_required(login_url='/blog/accounts/login/')
def feed_view(request):
    user = request.user
    following = user.posts.all()
    posts = []
    # TODO: Turn this into one line list comprehension.
    for post in Post.objects.all():
        if post.author in following:
            posts.append(post)
    return render(request, 'feed.html', {'title': 'Your Feed', 'posts': posts})


