from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers


from .views import (RegisterView, RegistePageView, show_register_page_view, CustomTokenView, UserPageView,
                    MemberPageView, ModeratorPageView,
                    UserListAPI, login_page,
                    showuserpage, verify_code_page, VerifyCodeAndRegisterAPIView, )
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('token/', CustomTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # مشاهده کاربران ثبت شده
    path('api/users/', UserListAPI.as_view(), name='user-list-api'),
    path('users/', UserPageView.as_view(), name='user_page'),
    path('show-users-page/', showuserpage, name='show_user_page'),
    #
    path('api/signup/', RegisterView.as_view(), name='apisignup'),
    path('signup/', RegistePageView.as_view(), name='signup'),
    path('show-signup-page/', show_register_page_view, name='show_signup_page'),
    #
    path('login-page/', login_page, name='login_page'),
    #
    # path('send-code/', VerifyCodeAndRegisterAPIView.as_view(), name='send_verification_code'),
    path('verify-code-api/', RegisterView.as_view(), name='verify_and_register_api'),
    #
    path('verify-api/', VerifyCodeAndRegisterAPIView.as_view(), name='verifi-api'),
    path('verify_code_page/', verify_code_page, name='verify-code-page'),
    #
    path('member/', MemberPageView.as_view(), name='member_page'),
    path('moderator/', ModeratorPageView.as_view(), name='moderator_page'),





]