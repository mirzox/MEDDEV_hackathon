from django.urls import path


from .views import LoginView, Logout, AccountDetailView, SendCode, VerifyCode, AddPatient

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', Logout.as_view()),
    # path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    # path('detail/', AccountView.as_view()),
    path('detail/', AccountDetailView.as_view()),
    path('sendcode/', SendCode.as_view()),
    path('verifyphone/', VerifyCode.as_view()),
    path('patient/', AddPatient.as_view())
]
