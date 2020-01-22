from django.urls import path
from accounts.views import LoginView, LogoutView, HomePageView


app_name = "accounts"


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('entrar/', LoginView.as_view(), name='entrar'),
    path('logout/', LogoutView.as_view(), name='logout'),
]