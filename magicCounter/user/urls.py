"""magicCounter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from user.views import CustomPasswordChangeView, CustomPasswordResetDoneView, \
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
from django.urls import path, include

from .views import signup, CustomPasswordResetView

urlpatterns = [
    path("inscription/", signup, name="user_signup"),
    # path("logout/", logout, name="user_logout"),
    path("password_change/", CustomPasswordChangeView.as_view(), name="user_password_change"),
    path("password_reset/", CustomPasswordResetView.as_view(), name="user_password_reset"),
    path("password_reset/done/", CustomPasswordResetDoneView.as_view(), name="user_password_reset_done"),
    path("reset/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name="user_password_reset_confirm"),
    path("reset/done/", CustomPasswordResetCompleteView.as_view(), name="user_password_reset_complete"),
]

