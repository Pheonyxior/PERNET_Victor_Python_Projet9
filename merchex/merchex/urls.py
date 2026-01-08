"""
URL configuration for merchex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('litrevu/', include('litrevu.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.conf import settings
from django.conf.urls.static import static

import authentication.views
import litrevu.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', LogoutView.as_view(
    ), name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('home/', litrevu.views.home, name='home'),
    
    path('tickets/', litrevu.views.ticket_list, name='ticket-list'),
    path('tickets/<int:id>/', litrevu.views.ticket_detail, name='ticket-detail'),
    path('tickets/add/', litrevu.views.ticket_create, name='ticket-create'),
    path('tickets/<int:id>/change/', litrevu.views.ticket_update, name='ticket-update'),
    path('tickets/<int:id>/delete/', litrevu.views.ticket_delete, name='ticket-delete'),

    path('reviews/', litrevu.views.review_list, name='review-list'),
    path('reviews/<int:id>/', litrevu.views.review_detail, name='review-detail'),
    path('reviews/add/', litrevu.views.review_create, name='review-create'),
    path('reviews/<int:id>/change/', litrevu.views.review_update, name='review-update'),
    path('reviews/<int:id>/delete/', litrevu.views.review_delete, name='review-delete'),

    # path('user_follows/', litrevu.views.user_follows_list, name='user_follows-list'),
    path('subscribe', litrevu.views.subscription, name='subscription'),
    path('unsubscribe/<int:id>/', litrevu.views.unsubscribe, name='unsubscription'),
    ]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )