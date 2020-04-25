from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .forms import TrainingForm
from .models import Training
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les principales stats pour le panel admin
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/home.html', locals())


class TrainingsView(LoginRequiredMixin, View):
    """
    Cette page permet de récupérer les formations en cours et en créer des nouvelles
    """
    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(TrainingsView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = TrainingForm()
        trainings = Training.objects.all()
        frees = Training.objects.filter(is_free=True).count()
        premiums = Training.objects.filter(is_free=False).count()
        return render(request, 'admin/trainings.html', locals())

    def post(self, request, *args, **kwargs):
        form = TrainingForm(request.POST)
        if form.is_valid():
            formation = form.save()
            messages.add_message(request, messages.SUCCESS, 'La formation "{}" a été créée.'.format(formation.name))
        return redirect('admin_trainings')

    def put(self, request, *args, **kwargs):
        training = get_object_or_404(Training, pk=request.POST['pk'])
        form = TrainingForm(request.POST, instance=training)
        if form.is_valid():
            formation = form.save()
            messages.add_message(request, messages.SUCCESS, 'La formation "{}" a été modifiée.'.format(formation.name))
        return redirect('admin_trainings')

    def delete(self, request, *args, **kwargs):
        training = get_object_or_404(Training, pk=request.POST['pk'])
        messages.add_message(request, messages.SUCCESS, 'La formation "{}" a été supprimée.'.format(training.name))
        training.delete()
        return redirect('admin_trainings')
