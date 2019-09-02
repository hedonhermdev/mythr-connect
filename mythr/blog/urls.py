from django.urls import path
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    path('', RedirectView.as_view(url='home/')),
    path('home/', views.home, name='blog-home'),
    path('feed/', views.feed_view, name='blog-feed')
]

urlpatterns += [
    path('accounts/register/', views.register_view, name='blog-accounts-register'),
    path('accounts/login/', views.login_view, name='blog-accounts-login'),
    path('accounts/logout/', views.logout_view, name='blog-accounts-logout'),
    path('accounts/profile/edit/', views.profile_edit_view, name='blog-accounts-edit'),
    path('accounts/user/<int:id>/', views.user_profile_view, name='blog-accounts-profile')]


urlpatterns += [
    path('accounts/user/<int:id>/follow/', views.user_follow_view, name='blog-accounts-profile-follow'),
    path('accounts/user/<int:id>/unfollow/', views.user_unfollow_view, name='blog-accounts-profile-unfollow')
]

urlpatterns += [
    path('post/new/', views.new_post_view, name='blog-post-new'),
    path('post/<int:id>/', views.post_detail_view, name='blog-post-detail'),
    path('post/<int:id>/edit/', views.post_edit_view, name='blog-post-edit'),
    path('post/<int:id>/comment/', views.new_comment_view, name='blog-post-comment'),
    path('post/<int:id>/delete/', views.post_delete_view, name='blog-post-delete')
]
