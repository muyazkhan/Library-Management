from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.UserLogin.as_view(),name="login"),
    path('logout/', views.UserLogout.as_view(),name="logout"),
    path('registration/', views.RegistrationView.as_view(),name="registration"),
    path('profile/', views.BookListView.as_view(), name='profile' ),
    path('edit_profile/', views.AccountUpdateView.as_view(), name="update_profile"),
]
   