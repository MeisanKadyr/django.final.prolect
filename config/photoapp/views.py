from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.views import View
from django.contrib.auth.models import User
from .models import Photo
from django.core.exceptions import PermissionDenied
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .models import Photo
from django.shortcuts import render, get_object_or_404


def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    return render(request, 'photoapp/photo_detail.html', {'photo': photo})

def download_photo(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)

    # Проверка, является ли текущий пользователь владельцем фотографии
    if request.user == photo.user:
        response = HttpResponse(photo.image, content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="{photo.image.name}"'
        return response
    else:
        return HttpResponseForbidden("You don't have permission to access this photo.")

class PhotoListView(ListView):
    model = Photo
    template_name = 'photoapp/list.html'
    context_object_name = 'photos'


class PhotoTagListView(PhotoListView):
    template_name = 'photoapp/taglist.html'

    def get_tag(self):
        return self.kwargs.get('tag')

    def get_queryset(self):
        return self.model.objects.filter(tags__slug=self.get_tag())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.get_tag()
        return context


class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photoapp/detail.html'
    context_object_name = 'photo'


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['title', 'description', 'image', 'tags']
    template_name = 'photoapp/create.html'
    success_url = reverse_lazy('photo:list')

    def form_valid(self, form):
        form.instance.submitter = self.request.user
        return super().form_valid(form)


class UserIsSubmitter(UserPassesTestMixin):
    def get_photo(self):
        return get_object_or_404(Photo, pk=self.kwargs.get('pk'))

    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user == self.get_photo().submitter
        else:
            raise PermissionDenied('Извините, у вас нет доступа')


class PhotoUpdateView(UserIsSubmitter, UpdateView):
    template_name = 'photoapp/update.html'
    model = Photo
    fields = ['title', 'description', 'tags']
    success_url = reverse_lazy('photo:list')


class PhotoDeleteView(UserIsSubmitter, DeleteView):
    template_name = 'photoapp/delete.html'
    model = Photo
    success_url = reverse_lazy('photo:list')
    
class DownloadImageView(View):
    def get(self, request, photo_id):
        photo = get_object_or_404(Photo, id=photo_id)
        user = request.user

        if user.is_authenticated and isinstance(user, User) and user.is_registered:
            response = HttpResponse(image.image_file.read(), content_type='photo/jpeg')
            response['Content-Disposition'] = f'attachment; filename={photo.filename}'
            return response
        else:
            return HttpResponseForbidden("Доступ запрещен")

class PhotoCreateView(LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        form.instance.submitter = self.request.user
        form.instance.save()

        self.request.user.uploaded_photos += 1
        self.request.user.save()

        messages.success(self.request, 'Фотография успешно загружена.')

        return super().form_valid(form)
