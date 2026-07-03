from django.contrib import admin
from django.urls import path, include
from poll import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.homeView, name='home'),
    path('register/', views.registrationView, name='registration'),
    path('verify-otp/', views.verifyOTPView, name='verify_otp'),
    path('login/', views.loginView, name='login'),
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('logout/', views.logoutView, name='logout'),
    path('position/', views.positionView, name='position'),
    path('candidate/<int:pos>/', views.candidateView, name='candidate'),
    path('candidate/detail/<int:id>/', views.candidateDetailView, name='detail'),
    path('result/', views.resultView, name='result'),
    path('changepass/', views.changePasswordView, name='changepass'),
    path('editprofile/', views.editProfileView, name='editprofile'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
