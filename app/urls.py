from django.urls import path
from .views import Home, Create, Update, Delete, Read, RegisterUser, Login, Logout, ChangePassword, HomeImportant, HomeNotImportant, HomeAlmostImportant, PasswordResetRequest, BaseUserDesc, SignOut
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

     path('', Home.as_view(), name='home'),
     path('important/', HomeImportant.as_view(), name='important'),
     path('almostimportant/', HomeAlmostImportant.as_view(), name='almostimportant'),
     path('notimportant/', HomeNotImportant.as_view(), name='notimportant'),
     path('create/', Create.as_view(), name='create'),
     path('register/', RegisterUser.as_view(), name='register'),
     path('login/', Login.as_view(), name='login'),
     path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
     path('password_change/', ChangePassword.as_view(), name="change_password"),
     path('password__changed/', TemplateView.as_view(template_name='registration/password_change_done.html'), name='password_changed'),
     path('password_reset/', PasswordResetRequest.as_view(), name='password_reset'),
     path('reset_done/', TemplateView.as_view(template_name='registration/password_reset_done.html'), name='reset_done'),
     path('update/<int:pk>', Update.as_view(), name='update'),#<int:pk> we have to put the argument given in the class(may be id, number) for pk of <int:pk>
     path('delete/<int:pk>', Delete.as_view(), name='delete'),
     path('read/<int:pk>', Read.as_view(), name='read'),
     path('password_reset_complete/', TemplateView.as_view(template_name="registration/reset_password_done.html"), name="password_reset_complete"),
     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
     path('user_info/', BaseUserDesc.as_view(), name='user_info'),
     path('user_delete/', SignOut.as_view(), name='sign_out')

]
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)