from tastypie.authorization import Authorization

class FolderAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)
    
    def read_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user
     
    def update_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user
    
    def delete_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)
    
    def delete_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

class TaskAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(folder__user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        return bundle.obj.folder.user == bundle.request.user

    def update_list(self, object_list, bundle):
        return object_list.filter(folder__user=bundle.request.user)
    
    def update_detail(self, object_list, bundle):
        print(object_list)
        return bundle.obj.folder.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        return object_list.filter(folder__user=bundle.request.user)
    
    def delete_detail(self, object_list, bundle):
        return bundle.obj.folder.user == bundle.request.user
