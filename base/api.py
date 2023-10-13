from django.http import Http404
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authentication import Authentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from django.contrib.auth.models import User
from base.models import Folder, Task
from tastypie.models import create_api_key
from django.urls import path
from tastypie.exceptions import BadRequest
from django.contrib.auth import login, logout, authenticate
from tastypie.models import ApiKey
from tastypie.http import HttpUnauthorized, HttpBadRequest
from .authorization import FolderAuthorization, TaskAuthorization


class UserLoginRegistrationResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'authentication'

    def prepend_urls(self):
        return [
            path('register/', self.wrap_view('register'), name="api_register"),
            path('login/', self.wrap_view('login'), name="api_login"),
            path('logout/', self.wrap_view('logout'), name="api_logout")
        ]

    def register(self, request, **kwargs):
        data = self.deserialize(request, request.body)
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = User.objects.create_user(username, password=password)
            return self.create_response(request, {'Successfully Registered'})
        else:
            return self.create_response(request, {'error': 'Username and password are required.'}, HttpBadRequest)

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body)
        username = data.get('username')
        password = data.get('password')
        if username is None or password is None:
            raise BadRequest('Please enter a value.')

        user = authenticate(username=username, password=password)
        if not user:
            raise BadRequest("Incorrect username or password.")
        login(request, user)
        try:
            api_key = ApiKey.objects.get(user=user)
            if not api_key.key:
                api_key.save()
        except ApiKey.DoesNotExist:
            api_key = ApiKey.objects.create(user=user)

        return self.create_response(request, {
                'success': True,
                'username':username,
                'token': api_key.key
            })

    def logout(self, request, **kwargs):
        # self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated:
            logout(request)
            return self.create_response(request, 'Logged Out')
        else:
            return self.create_response(request, "Logout Error")

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        # excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        

class FolderResource(ModelResource):
    user = fields.ForeignKey(UserResource, attribute='user',null=True, full=True)
    shared_with = fields.ManyToManyField(UserResource, attribute='shared_with',null=True)
    class Meta:
        queryset = Folder.objects.all()
        resource_name = 'folder'
        authentication = ApiKeyAuthentication()
        authorization = FolderAuthorization()

    def prepend_urls(self):
        return [
            path('folder/<int:pk>/share/', self.wrap_view('share_folder'), name="api_share_folder"),
            path('folder/<int:pk>/unshare/', self.wrap_view('unshare_folder'), name="api_unshare_folder"),
        ]

    def share_folder(self, request, **kwargs):
        folder = Folder.objects.get(pk=kwargs['pk'])
        if not (request.user == folder.user):
            return self.create_response(request, {'error': 'Permission denied.'}, HttpUnauthorized)

        data = self.deserialize(request, request.body)
        user_id = data.get('user_id')

        if not user_id:
            return self.create_response(request, {'error': 'User ID is required.'}, HttpBadRequest)

        user = User.objects.filter(pk=user_id).first()
        if not user:
            return self.create_response(request, {'error': 'User not found.'}, HttpBadRequest)

        folder.shared_with.add(user)
        folder.save()
        return self.create_response(request, {'Successfully shared the folder with the user'})       

    def unshare_folder(self, request, **kwargs):
        folder = Folder.objects.get(pk=kwargs['pk'])

        if not (request.user == folder.user):
            return self.create_response(request, {'error': 'Permission denied.'}, HttpUnauthorized)

        data = self.deserialize(request, request.body)
        user_id = data.get('user_id')
        if not user_id:
            return self.create_response(request, {'error': 'User ID is required.'}, HttpBadRequest)

        user = User.objects.filter(pk=user_id).first()
        if not user:
            return self.create_response(request, {'error': 'User not found.'}, HttpBadRequest)

        folder.shared_with.remove(user)
        folder.save()
        return self.create_response(request, {'Successfully un-shared the folder with the user'})


class TaskResource(ModelResource):
    folder = fields.ForeignKey(FolderResource, attribute='folder')
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'task'
        authentication = ApiKeyAuthentication()
        authorization = TaskAuthorization()
        filtering = {
            "folder": ('exact', ),
        }