from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .views import*

urlpatterns =[
    path('', login_required(home), name='home'),
    path('paste/', login_required(paste_link), name='paste_link'),
    path('predict_link/', login_required(predict_link), name='predict_link'),
    path('paste', login_required(paste_ip), name='paste_ip'),
    path('realtime_click/', login_required(realtime_click), name='realtime_click'),
    path('realtime_click_test/', login_required(realtime_click_test), name='realtime_click_test'),
    path('complaints/register/', login_required(complaint_register), name='complaint_register'),
    path('complaints/', login_required(complaint_list), name='complaint_list'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
]
