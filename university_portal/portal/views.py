from django.shortcuts import render
from rest_framework import viewsets
from .models import Announcement, Event, ScientificIdea, Comment
from .serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsModerator, IsMember, IsUser
class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAuthenticated(), IsModeratorOrMember()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAuthenticated(), IsModeratorOrMember()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ScientificIdeaViewSet(viewsets.ModelViewSet):
    queryset = ScientificIdea.objects.all()
    serializer_class = ScientificIdeaSerializer

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT']:
            return [IsAuthenticated(), IsModerator()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




def login_page(request):
    return render(request, 'portal/login.html')


def perform_create(self, serializer):
    serializer.save(submitted_by=self.request.user)




#


# داشبورد کاربر عادی
class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsUser]

    def get(self, request):
        return Response({
            "role": "user",
            "message": "داشبورد کاربر عادی",
            "available_actions": [
                "مشاهده اطلاعیه‌ها",
                "مشاهده رویدادها",
                "ارسال ایده یا مقاله علمی",
                "ثبت نظر برای رویداد یا اطلاعیه"
            ]
        })


# داشبورد عضو انجمن
class MemberDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsMember]

    def get(self, request):
        return Response({
            "role": "member",
            "message": "داشبورد عضو انجمن",
            "available_actions": [
                "ایجاد اطلاعیه",
                "ویرایش یا حذف اطلاعیه",
                "ثبت رویداد جدید",
                "مدیریت نظرات"
            ]
        })


# داشبورد مدیر انجمن
class ModeratorDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsModerator]

    def get(self, request):
        return Response({
            "role": "moderator",
            "message": "داشبورد مدیر انجمن",
            "available_actions": [
                "تمام دسترسی‌های عضو انجمن",
                "تأیید و انتشار مقالات علمی",
                "حذف کاربران",
                "مدیریت کامل محتوا"
            ]
        })


def member_dashboard_page(request):
    return render(request, 'portal/member_dashboard.html')
