import uuid
from rest_framework import serializers
# from drf_extra_fields.fields import Base64FileField
from apps.users.models import User
from .models import ForgejoProfile


class ForgejoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForgejoProfile
        fields = '__all__'


class ForgejoUserPreCreSerializer(serializers.Serializer):
    created_at = serializers.CharField(required=False)
    email = serializers.EmailField()
    full_name = serializers.CharField(required=False)
    login_name = serializers.CharField(required=False)
    must_change_password = serializers.BooleanField(required=False, default=False)
    password = serializers.CharField(required=False, min_length=5)
    restricted = serializers.BooleanField(required=False)
    send_notify = serializers.BooleanField(required=False)
    source_id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=False)
    visibility = serializers.CharField(required=False)

    def validate(self, attrs):
        if 'password' not in attrs:
            attrs['password'] = User.objects.filter(email=attrs['email']).first().password
        if 'username' not in attrs:
            attrs['username'] = attrs['email'].split('@')[0]
        if 'login_name' not in attrs:
            attrs['login_name'] = attrs['email'].split('@')[0]
        return attrs


class ForgejoUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForgejoProfile
        fields = '__all__'

    def validate(self, attrs):
        if 'user_id' not in attrs:
            attrs['user_id'] = User.objects.filter(email=attrs['email']).first().pk
        return attrs

    def create(self, validated_data):
        if 'user_id' not in validated_data:
            user = ForgejoProfile(
                user_id=User.objects.get(email=validated_data['email']).pk,
                # forgejo_id=validated_data['id'],
                username=validated_data['login']
            )
        else:
            user = ForgejoProfile(
                user_id=validated_data['user_id'],
                # forgejo_id=validated_data.get('id'),
                username=validated_data['username']
            )
        user.save()
        return user


class ForgejoGetProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    login = serializers.CharField(required=False)
    login_name = serializers.CharField(required=False)
    full_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    avatar_url = serializers.CharField(required=False)
    language = serializers.CharField(required=False)
    is_admin = serializers.BooleanField(required=False)
    last_login = serializers.DateTimeField(required=False)
    created	= serializers.DateTimeField(required=False)
    restricted = serializers.BooleanField(required=False)
    active = serializers.BooleanField(required=False)
    prohibit_login = serializers.BooleanField(required=False)
    location = serializers.CharField(required=False)
    website	= serializers.CharField(required=False)
    visibility = serializers.CharField(required=False)
    followers_count = serializers.IntegerField(required=False)
    following_count = serializers.IntegerField(required=False)
    starred_repos_count = serializers.IntegerField(required=False)
    username = serializers.CharField(required=False)


class CreateRepositorySerializer(serializers.Serializer):
    auto_init = serializers.BooleanField(required=False)
    default_branch = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    gitignores = serializers.CharField(required=False)
    issue_labels = serializers.CharField(required=False)
    license = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    private	= serializers.BooleanField(required=False)
    readme = serializers.CharField(required=False)
    template = serializers.BooleanField(required=False)
    trust_model = serializers.ChoiceField(choices=['default', 'collaborator', 'committer', 'collaboratorcommitter'], required=False)
    
    def validate(self, attrs):
        if 'name' not in attrs:
            attrs['name'] = 'diplom'
        if ' ' in attrs['name']:
            attrs['name'].replace(' ', '-')
        return attrs


class Identify(serializers.Serializer):
    email = serializers.EmailField(required=False)
    name = serializers.CharField(required=False)
    
class CommitDateOptions(serializers.Serializer):
    author = serializers.CharField(required=False)
    committer = serializers.CharField(required=False)


class CreateFileOptionsSerializer(serializers.Serializer):
    author = Identify(required=False)
    branch = serializers.CharField(required=False)
    committer = Identify(required=False)
    content = serializers.CharField(help_text='content must be base64 encoded', required=False)
    dates = CommitDateOptions(required=False)
    message = serializers.CharField(required=False)
    new_branch = serializers.CharField(required=False)
    signoff = serializers.BooleanField(required=False)


class UpdateFileOptionsSerializer(serializers.Serializer):
    author = Identify(required=False)
    branch = serializers.CharField(required=False)
    committer = Identify(required=False)
    content = serializers.CharField(help_text='content must be base64 encoded')
    dates = CommitDateOptions(required=False)
    from_path = serializers.CharField(required=False)
    message = serializers.CharField(required=False)
    new_branch = serializers.CharField(required=False)
    sha = serializers.CharField(required=False)
    signoff = serializers.BooleanField(required=False)
