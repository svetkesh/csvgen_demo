from django.shortcuts import render, get_object_or_404, redirect
from .forms import SchemaForm, ColumnForm
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from celery.result import AsyncResult
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from .tasks import generate_csv
from django.contrib.auth.models import User


from .models import Schema, Column


class SchemaListView(LoginRequiredMixin, ListView):
    login_url = 'accounts/login/'
    model = Schema

    def get_queryset(self):
        return Schema.objects.filter(
            author=self.request.user
        )


class SchemaDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Schema


class CreateSchemaView(LoginRequiredMixin, CreateView):
    login_url = 'accounts/login/'
    redirect_field_name = 'maker/schema_detail.html'
    form_class = SchemaForm
    model = Schema

    exclude = ['author']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class SchemaUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'accounts/login/'
    redirect_field_name = 'maker/schema_detail.html'
    form_class = SchemaForm
    model = Schema


class SchemaDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'accounts/login/'
    model = Schema
    success_url = reverse_lazy('schema_list')


@login_required
def add_column_to_schema(request, pk):
    schema = get_object_or_404(Schema, pk=pk)
    if request.method == "POST":
        form = ColumnForm(request.POST)
        if form.is_valid():
            column = form.save(commit=False)
            column.schema = schema
            column.save()
            return redirect('schema_detail', pk=schema.pk)
        else:
            form = ColumnForm()
    else:
        form = ColumnForm()
    return render(request, 'maker/column_form.html', {'form': form})


@login_required
def column_edit(request, pk):
    column = get_object_or_404(Column, pk=pk)
    if request.method == "POST":
        form = ColumnForm(request.POST, instance=column)
        if form.is_valid():
            column = form.save(commit=False)
            column.author = request.user
            column.save()
            return redirect('schema_detail', pk=column.schema.pk)
    else:
        form = ColumnForm(instance=column)
    return render(request, 'maker/column_form.html', {'form': form})


@login_required
def column_remove(request, pk):
    column = get_object_or_404(Column, pk=pk)
    schema_pk = column.schema.pk
    column.delete()
    return redirect('schema_detail', pk=schema_pk)


# ajax processing
@csrf_exempt
def run_task(request):
    if request.POST:
        schemas = User.objects.get(pk=request.user.id).schema_set.all()
        quantity = int(request.POST.get('quantity'))

        tasks_dict = {}
        for schema in schemas:
            task = generate_csv.delay(
                schema.id,
                quantity
            )
            tasks_dict[schema.id] = task.id
        return JsonResponse(tasks_dict, status=202)


@csrf_exempt
def get_status(request, task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JsonResponse(result, status=200)
