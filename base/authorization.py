from tastypie.authorization import Authorization
from django.db.models import Q


class FolderAuthorization(Authorization):
    # # Able to fetch own folder and shared folders
    # def read_list(self, object_list, bundle):
    #     return object_list.filter(Q(user=bundle.request.user) | Q(shared_with=bundle.request.user)).distinct()

    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        return (bundle.request.user in bundle.obj.shared_with.all()) or bundle.obj.user == bundle.request.user

    # # Able to update own folder and shared folders
    # def update_list(self, object_list, bundle):
    #     return object_list.filter(Q(user=bundle.request.user) | Q(shared_with=bundle.request.user)).distinct()

    def update_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)

    def update_detail(self, object_list, bundle):
        return (bundle.request.user in bundle.obj.shared_with.all()) or bundle.obj.user == bundle.request.user

    # # Able to delete own folder and shared folders
    # def delete_list(self, object_list, bundle):
    #     return object_list.filter(Q(user=bundle.request.user) | Q(shared_with=bundle.request.user)).distinct()

    def delete_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)

    def delete_detail(self, object_list, bundle):
        return (bundle.request.user in bundle.obj.shared_with.all()) or bundle.obj.user == bundle.request.user

class TaskAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # return object_list.filter(folder__user=bundle.request.user)
        return object_list.filter(Q(folder__user=bundle.request.user) | Q(folder__shared_with=bundle.request.user)).distinct()

    def read_detail(self, object_list, bundle):
        return bundle.obj.folder.user == bundle.request.user or (bundle.request.user in bundle.obj.folder.shared_with.all())

    def update_list(self, object_list, bundle):
        return object_list.filter(folder__user=bundle.request.user)

    def update_detail(self, object_list, bundle):
        return bundle.obj.folder.user == bundle.request.user or (bundle.request.user in bundle.obj.folder.shared_with.all())

    def delete_list(self, object_list, bundle):
        return object_list.filter(folder__user=bundle.request.user)

    def delete_detail(self, object_list, bundle):
        return bundle.obj.folder.user == bundle.request.user or (bundle.request.user in bundle.obj.folder.shared_with.all())
