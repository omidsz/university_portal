from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet)
router.register(r'events', EventViewSet)
router.register(r'ideas', ScientificIdeaViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_page, name='login-html'),
    path('dashboard/user/', UserDashboardView.as_view(), name='dashboard-user'),
    path('dashboard/member/', MemberDashboardView.as_view(), name='dashboard-member'),
    path('dashboard/moderator/', ModeratorDashboardView.as_view(), name='dashboard-moderator')
]

urlpatterns += [
    path('dashboard-page/member/', member_dashboard_page, name='member-dashboard-page'),
]