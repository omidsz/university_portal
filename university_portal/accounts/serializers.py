from rest_framework import serializers
from django.contrib.auth.models import User

from .models import EmailVerificationCode

from django.utils import timezone
from django.core.mail import send_mail
import random


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        return user

###################################################################################


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')

        # بررسی وجود رکورد کد تأیید
        try:
            record = EmailVerificationCode.objects.get(email=email)
        except EmailVerificationCode.DoesNotExist:
            raise serializers.ValidationError({'code': 'کد تأیید نادرست است.'})

        # بررسی منقضی بودن کد
        if record.is_expired():
            raise serializers.ValidationError({'code': 'کد منقضی شده است.'})

        # بررسی مطابقت کد
        if record.code != code:
            raise serializers.ValidationError({'code': 'کد وارد شده صحیح نیست.'})

        return attrs


class EmailSendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        email = validated_data['email']
        code = str(random.randint(100000, 999999))

        send_mail(
            subject='کد تأیید ایمیل',
            message=f'کد شما: {code}',
            from_email='omidsoozice@gmail.com',
            recipient_list=[email],
            fail_silently=False,
        )

        # اگر کدی برای این ایمیل وجود دارد، آپدیت کن
        verification, created = EmailVerificationCode.objects.update_or_create(
            email=email,
            defaults={'code': code, 'created_at': timezone.now()}
        )

        # ارسال ایمیل را اینجا اضافه کن (توضیح پایین)
        print(f"Send this code to email: {code}")  # برای تست

        return verification


class EmailVerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            verification = EmailVerificationCode.objects.get(email=data['email'], code=data['code'])
        except EmailVerificationCode.DoesNotExist:
            raise serializers.ValidationError("کد یا ایمیل نادرست است.")

        if verification.is_expired():
            raise serializers.ValidationError("کد منقضی شده است.")

        return data


