# from typing import Any
# from django.shortcuts import render, redirect
# from django.views.generic.list import ListView
# from django.views.generic.edit import CreateView, DeleteView, FormView
# from .models import Folder, Task
# from django.urls import reverse_lazy
# from django.contrib.auth.views import LoginView
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth import login


# class CustomLoginView(LoginView):
#     template_name = 'base/login.html'
#     fields = "__all__"
#     redirect_authenticated_user = True

#     def get_success_url(self):
#         return reverse_lazy('folders')
    
# class RegisterPage(FormView):
#     template_name = 'base/register.html'
#     form_class = UserCreationForm
#     redirect_authenticated_user = True
#     success_url = reverse_lazy('folders')

#     def form_valid(self, form):
#         user = form.save()
#         if user is not None:
#             login(self.request, user)
#         return super(RegisterPage, self).form_valid(form)
    
#     def get(self, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             return redirect('folders')
#         return super(RegisterPage, self).get(*args, **kwargs)

# class FolderList(LoginRequiredMixin, ListView):
#     model = Folder
#     context_object_name = 'folders'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['folders'] = context['folders'].filter(user=self.request.user)
#         # context['count'] = context['folders'].filter(complete=False).count()
#         return context


# class FolderCreate(LoginRequiredMixin, CreateView):
#     model = Folder
#     fields = ['title']
#     success_url = reverse_lazy('folders')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(FolderCreate, self).form_valid(form)

# class TaskCreate(LoginRequiredMixin, CreateView):
#     model = Task
#     fields = ['title', 'description', 'complete']
#     success_url = reverse_lazy('folders')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(FolderCreate, self).form_valid(form)
    

# class DeleteView(LoginRequiredMixin, DeleteView):
#     model = Folder
#     context_object_name = 'folder'
#     success_url = reverse_lazy('folders')
#     template_name = 'base/folder_delete.html'