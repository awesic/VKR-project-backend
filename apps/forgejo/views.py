import base64
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics, parsers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from apps.users.permissions import IsStudent, IsTeacher
from .serializers import (
    ForgejoUserCreateSerializer,
    ForgejoUserPreCreSerializer,
    ForgejoUserSerializer,
    ForgejoGetProfileSerializer,
    CreateRepositorySerializer,
    CreateFileOptionsSerializer,
    UpdateFileOptionsSerializer,
    )
from .models import ForgejoProfile
from .services import (
    create_forgejo,
    create_forgejo_repo,
    delete_forgejo_user,
    get_forgejo_user,
    get_forgejo_repo,
    upload_get_file_to_repo,
    docx_to_html,
    )


class ForgejoProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ForgejoProfile.objects.all()
    serializer_class = ForgejoUserSerializer
    permission_classes = [IsStudent | IsAdminUser]
    my_tags = ['forgejo']

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated, ]
        return super().get_permissions()
    
    def retrieve(self, request, *args, **kwargs):
        try:
            user_id = get_user_model().objects.filter(email=kwargs.get('email')).first().pk
            forgejo_user = get_forgejo_user(kwargs.get('email'))
            forgejo_serializer = ForgejoGetProfileSerializer(forgejo_user, many=False)
            return Response(forgejo_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        user_id = get_user_model().objects.filter(email=kwargs.get('email')).first().pk
        forgejo = self.queryset.filter(user_id=user_id).first()
        if forgejo:
            try:
                delete_forgejo_user(username=forgejo.username)
                forgejo.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response(e.args, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(
    name='post', 
    decorator=swagger_auto_schema(
        operation_summary='Create forgejo profile', 
        request_body=ForgejoUserPreCreSerializer, 
        responses={201: ForgejoUserSerializer}))
#@method_decorator(
#    name='get',
#    decorator=swagger_auto_schema(operation_summary='Get forgejo profiles',
#    manual_parameters=[
#        openapi.Parameter('source_id', openapi.IN_QUERY, description="ID of the user's login source to search for", type=openapi.TYPE_INTEGER),
#        openapi.Parameter('login_name', openapi.IN_QUERY, description="user's login name to search for", type=openapi.TYPE_STRING),
#        openapi.Parameter('page', openapi.IN_QUERY, description="page number of results to return (1-based)", type=openapi.TYPE_INTEGER),
#        openapi.Parameter('limit', openapi.IN_QUERY, description="page size of results", type=openapi.TYPE_INTEGER),
#        ],
#    responses={200: ForgejoGetProfileSerializer})
#)
class ForgejoProfileCreateView(generics.CreateAPIView):
    queryset = ForgejoProfile.objects.all()
    serializer_class = ForgejoUserSerializer
    permission_classes = [IsStudent | IsAdminUser]
    my_tags = ['forgejo']
    
    # def list(self, request, *args, **kwargs):
    #     try:
    #         params = {}
    #         if request.query_params:
    #             params = request.query_params.dict()
    #         users = get_forgejo_user(params)
    #         if users:
    #             users = ForgejoGetProfileSerializer(users, many=True)
    #             return Response(users.data, status=status.HTTP_200_OK)
    #         return Response(users, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        user_id = get_user_model().objects.filter(
            email=request.get('email').first().pk
        )
        try:
            forgejo_user = create_forgejo(request.data, user_id, *args, **kwargs)
            return Response(forgejo_user, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)


class CreateRepositoryView(generics.UpdateAPIView):
    serializer_class = CreateRepositorySerializer
    queryset = ForgejoProfile.objects.all()
    permission_classes = [IsStudent | IsAdminUser | IsTeacher]
    my_tags = ['forgejo']
    
    def partial_update(self, request, *args, **kwargs):
        forgejo = self.queryset.filter(user_id=get_user_model().objects.filter(email=kwargs.get('email')).first().pk).first()
        create_serializer = self.serializer_class(data=request.data)
        if create_serializer.is_valid() and forgejo:
            serializer = ForgejoUserSerializer(forgejo, data={'repo_name': create_serializer.validated_data['name']}, partial=True)
            forgejo_repo = create_forgejo_repo(username=forgejo.username, data=create_serializer.data)
            if serializer.is_valid() and forgejo_repo:
                serializer.save()
                return Response(forgejo_repo, status=status.HTTP_201_CREATED)
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': create_serializer.errors if forgejo else 'Forgejo user not found'}, status=status.HTTP_400_BAD_REQUEST)


class ListRepositoryView(generics.ListAPIView):
    serializer_class = CreateRepositorySerializer
    queryset = ForgejoProfile.objects.all()
    permission_classes = [IsStudent | IsAdminUser]
    my_tags = ['forgejo']
    
    def list(self, request, *args, **kwargs):
        forgejo = self.queryset.filter(user_id=get_user_model().objects.filter(email=kwargs.get('email')).first().pk).first()
        try:
            repos = get_forgejo_repo(username=forgejo.username, repo=kwargs.get('repo'))
            return Response(repos, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args if forgejo else {'message': 'Forgejo user not found'}, status=status.HTTP_400_BAD_REQUEST)


# @method_decorator(
#     name='post', 
#     decorator=swagger_auto_schema(
#         operation_summary='Add file to repository', 
#         # request_body=CreateFileOptionsSerializer, 
#         # responses={201: ForgejoUserSerializer}
#         ))
# @method_decorator(
#     name='get',
#     decorator=swagger_auto_schema(operation_summary='Get forgejo profiles',
#     manual_parameters=[
#         openapi.Parameter('source_id', openapi.IN_QUERY, description="ID of the user's login source to search for", type=openapi.TYPE_INTEGER),
#         openapi.Parameter('login_name', openapi.IN_QUERY, description="user's login name to search for", type=openapi.TYPE_STRING),
#         openapi.Parameter('page', openapi.IN_QUERY, description="page number of results to return (1-based)", type=openapi.TYPE_INTEGER),
#         openapi.Parameter('limit', openapi.IN_QUERY, description="page size of results", type=openapi.TYPE_INTEGER),
#         ],
#     responses={200: ForgejoGetProfileSerializer})
# )
class UploadFileRepositoryView(generics.CreateAPIView,
                               generics.RetrieveUpdateAPIView
                               ):
    # serializer_class = CreateFileOptionsSerializer
    queryset = ForgejoProfile.objects.all()
    permission_classes = [IsStudent | IsAdminUser | IsTeacher]
    parser_classes = [parsers.MultiPartParser]
    my_tags = ['forgejo']
    
    def retrieve(self, request, *args, **kwargs):
        forgejo = self.queryset.filter(user_id=get_user_model().objects.filter(email=kwargs.get('email')).first().pk).first()
        try:
            params = {} if not request.query_params else request.query_params.dict()
            response = upload_get_file_to_repo(
                username=forgejo.username,
                repo=kwargs.get('repo'),
                filepath=kwargs.get('filepath'),
                params=params
            )
            data = response.copy()
            data.pop('sha')
            if data['content']: 
                data['content'] = base64.b64decode(response.get('content')).decode()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
        
    def create(self, request, *args, **kwargs):
        forgejo = self.queryset.filter(user_id=get_user_model().objects.filter(email=kwargs.get('email')).first().pk).first()
        serializer = CreateFileOptionsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                if not forgejo.repo_name and forgejo:
                    repo_name = 'diplom'
                    fu_serializer = ForgejoUserSerializer(forgejo, data={'repo_name': repo_name}, partial=True)
                    forgejo_repo = create_forgejo_repo(username=forgejo.username, data={'name': repo_name})
                    if fu_serializer.is_valid() and forgejo_repo:
                        fu_serializer.save()
                
                file = request.FILES.get('file', None)
                if file:
                    file = file.read()
                else:
                    file = request.data['content']
                    
                serializer.validated_data['content'] = str(base64.b64encode(file.encode()))[2:-1]

                response = upload_get_file_to_repo(
                    username=forgejo.username, 
                    repo=kwargs.get('repo'), 
                    filepath=kwargs.get('filepath'),
                    data=serializer.validated_data,
                    method='POST')
                forgejo_serializer = ForgejoUserSerializer(
                    forgejo, 
                    data={'last_commit_id': response.get('commit')['sha'],
                        'sha': response.get('content')['sha']}, 
                    partial=True)
                if forgejo_serializer.is_valid():
                    forgejo_serializer.save()
                    
                response_data = response.get('content')
                response_data.pop('sha')
                if response_data['content']: 
                    response_data['content'] = base64.b64decode(response_data.get('content')).decode()
                return Response(response_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': serializer.errors if forgejo else 'Forgejo user not found'}, 
            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        forgejo = self.queryset.filter(user_id=get_user_model().objects.filter(email=kwargs.get('email')).first().pk).first()
        serializer = UpdateFileOptionsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                if not forgejo.repo_name and forgejo:
                    repo_name = 'diplom'
                    fu_serializer = ForgejoUserSerializer(forgejo, data={'repo_name': repo_name}, partial=True)
                    forgejo_repo = create_forgejo_repo(username=forgejo.username, data={'name': repo_name})
                    if fu_serializer.is_valid() and forgejo_repo:
                        fu_serializer.save()
                if forgejo:
                    file_content = request.data['content']
                        
                    serializer.validated_data['content'] = str(base64.b64encode(file_content.encode()))[2:-1]
                    if 'sha' not in serializer.validated_data:
                        serializer.validated_data['sha'] = forgejo.sha

                    response = upload_get_file_to_repo(
                        username=forgejo.username,
                        repo=kwargs.get('repo'),
                        filepath=kwargs.get('filepath'),
                        data=serializer.validated_data,
                        method='PUT'
                    )
                    forgejo_serializer = ForgejoUserSerializer(
                        forgejo, 
                        data={'last_commit_id': response.get('commit')['sha'],
                            'sha': response.get('content')['sha']}, 
                        partial=True)
                    if forgejo_serializer.is_valid():
                        forgejo_serializer.save()
                    
                    data = response.get('content')
                    data.pop('sha')
                    if data['content']: 
                        data['content'] = base64.b64decode(data.get('content')).decode()
                    return Response(data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)


class UploadFileToForgejo(generics.CreateAPIView,
                          generics.UpdateAPIView):
    queryset = ForgejoProfile.objects.all()
    permission_classes = [IsStudent | IsAdminUser | IsTeacher]
    my_tags = ['forgejo']
    
    def create(self, request, *args, **kwargs):
        forgejo = self.queryset.filter(user_id=get_user_model().objects.filter(email=kwargs.get('email')).first().pk).first()
        try:
            if not forgejo.repo_name and forgejo:
                repo_name = 'diplom'
                serializer = ForgejoUserSerializer(forgejo, data={'repo_name': repo_name}, partial=True)
                forgejo_repo = create_forgejo_repo(username=forgejo.username, data={'name': repo_name})
                if serializer.is_valid() and forgejo_repo:
                    serializer.save()
            if forgejo:
                file = request.FILES['file']

                if file:
                    urls = f'{settings.MEDIA_ROOT}fileload/'
                    fs = FileSystemStorage(location=urls, base_url=urls)
                    filename = fs.save(file.name, file)
                    filepath = urls + file.name

                    result = docx_to_html(filepath)
                    fs.delete(filename)
                    
                    result['author'] = {'email': kwargs.get('email')}
                    result['committer'] = {'email': kwargs.get('email')}
                    result['content'] = str(base64.b64encode(result.pop('data').encode()))[2:-1]

                    create_serializer = CreateFileOptionsSerializer(data=result)
                    if create_serializer.is_valid():
                        response = upload_get_file_to_repo(
                            username=forgejo.username,
                            repo=kwargs.get('repo'),
                            filepath='diplom.html',
                            data=create_serializer.validated_data,
                            method='POST')
                        forgejo_serializer = ForgejoUserSerializer(
                            forgejo, 
                            data={'last_commit_id': response.get('commit')['sha'],
                                'sha': response.get('content')['sha']}, 
                            partial=True)
                        if forgejo_serializer.is_valid():
                            forgejo_serializer.save()
                        
                        return Response({'message': 'Файл успешно загружен!'}, status=status.HTTP_201_CREATED)
  
                    return Response({'message': create_serializer.errors.get('content')}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Bad request!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': e.args}, status=status.HTTP_400_BAD_REQUEST)
