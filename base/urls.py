from django.urls import path, include
from .api import FolderResource, UserResource, TaskResource, UserLoginRegistrationResource
from django.contrib.auth.views import LogoutView


folder_resource = FolderResource()
user_registration_resource = UserLoginRegistrationResource()
user_resource = UserResource()
task_resource = TaskResource()

urlpatterns = [

    path('', include(folder_resource.urls)),
    path('', include(task_resource.urls)),
    path('', include(user_registration_resource.urls)),
    path('', include(user_resource.urls)),

]