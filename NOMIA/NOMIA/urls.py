from django.contrib import admin
from django.urls import path
from QUESTIONS import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home_page'),
    path('survey/<str:survey>/<int:question_number>', views.survey, name='survey'),
    path('error', views.error, name='error'),
    path('user_login/', auth_views.LoginView.as_view(template_name='user_login.html'), name='user_login'),
    path('user_logout/', auth_views.LogoutView.as_view(template_name='user_logout.html'), name='user_logout'),
]
# Если я захочу использовать logout, то используй версию Django позже чем 5.0.1,
# а лучше 4.1.7, потому что в 5.0.1 убирается выход через get