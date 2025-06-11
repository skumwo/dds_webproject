from django.shortcuts import render, get_object_or_404, redirect
from .models import CashFlowRecord, Status, Type, Category, SubCategory
from .forms import CashFlowRecordForm
from django import forms
from django.db.models import Q
from django.http import JsonResponse

class CashFlowFilterForm(forms.Form):
    date_from = forms.DateField(required=False, label="С")
    date_to = forms.DateField(required=False, label="По")
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=False)
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    subcategory = forms.ModelChoiceField(queryset=SubCategory.objects.all(), required=False)

def cashflow_list(request):
    form = CashFlowFilterForm(request.GET or None)
    qs = CashFlowRecord.objects.all().select_related('status', 'type', 'category', 'subcategory')
    if form.is_valid():
        if form.cleaned_data['date_from']:
            qs = qs.filter(created_at__gte=form.cleaned_data['date_from'])
        if form.cleaned_data['date_to']:
            qs = qs.filter(created_at__lte=form.cleaned_data['date_to'])
        if form.cleaned_data['status']:
            qs = qs.filter(status=form.cleaned_data['status'])
        if form.cleaned_data['type']:
            qs = qs.filter(type=form.cleaned_data['type'])
        if form.cleaned_data['category']:
            qs = qs.filter(category=form.cleaned_data['category'])
        if form.cleaned_data['subcategory']:
            qs = qs.filter(subcategory=form.cleaned_data['subcategory'])
    return render(request, 'dds/cashflow_list.html', {'records': qs, 'form': form})

def cashflow_create(request):
    if request.method == 'POST':
        form = CashFlowRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cashflow_list')
    else:
        form = CashFlowRecordForm()
    return render(request, 'dds/cashflow_form.html', {'form': form, 'title': 'Добавить запись'})

def cashflow_edit(request, pk):
    record = get_object_or_404(CashFlowRecord, pk=pk)
    if request.method == 'POST':
        form = CashFlowRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('cashflow_list')
    else:
        form = CashFlowRecordForm(instance=record)
    return render(request, 'dds/cashflow_form.html', {'form': form, 'title': 'Редактировать запись'})

def cashflow_delete(request, pk):
    record = get_object_or_404(CashFlowRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('cashflow_list')

from django.db.models import ProtectedError
from django.contrib import messages

def dicts_unified(request):
    # Удаление с обработкой ошибок
    for model, prefix, name in [
        (Status, 'del_status', 'статус'),
        (Type, 'del_type', 'тип'),
        (Category, 'del_category', 'категория'),
        (SubCategory, 'del_subcategory', 'подкатегория'),
    ]:
        obj_id = request.POST.get(prefix)
        if obj_id:
            try:
                model.objects.filter(pk=obj_id).delete()
                messages.success(request, f"{name.capitalize()} успешно удалён(а).")
            except ProtectedError:
                messages.error(
                    request,
                    f"Невозможно удалить: {name} используется в других записях."
                )
            return redirect('dicts_unified')

    # Добавление и редактирование
    if request.method == 'POST':
        if 'add_status' in request.POST:
            name = request.POST.get('status_name')
            if name:
                Status.objects.create(name=name)
                messages.success(request, "Статус добавлен.")
            return redirect('dicts_unified')
        if 'edit_status' in request.POST:
            pk = request.POST.get('edit_status')
            name = request.POST.get('status_name')
            if pk and name:
                Status.objects.filter(pk=pk).update(name=name)
                messages.success(request, "Статус изменён.")
            return redirect('dicts_unified')

        if 'add_type' in request.POST:
            name = request.POST.get('type_name')
            if name:
                Type.objects.create(name=name)
                messages.success(request, "Тип добавлен.")
            return redirect('dicts_unified')
        if 'edit_type' in request.POST:
            pk = request.POST.get('edit_type')
            name = request.POST.get('type_name')
            if pk and name:
                Type.objects.filter(pk=pk).update(name=name)
                messages.success(request, "Тип изменён.")
            return redirect('dicts_unified')

        if 'add_category' in request.POST:
            name = request.POST.get('category_name')
            type_id = request.POST.get('category_type')
            if name and type_id:
                Category.objects.create(name=name, type_id=type_id)
                messages.success(request, "Категория добавлена.")
            return redirect('dicts_unified')
        if 'edit_category' in request.POST:
            pk = request.POST.get('edit_category')
            name = request.POST.get('category_name')
            type_id = request.POST.get('category_type')
            if pk and name and type_id:
                Category.objects.filter(pk=pk).update(name=name, type_id=type_id)
                messages.success(request, "Категория изменена.")
            return redirect('dicts_unified')

        if 'add_subcategory' in request.POST:
            name = request.POST.get('subcategory_name')
            category_id = request.POST.get('subcategory_category')
            if name and category_id:
                SubCategory.objects.create(name=name, category_id=category_id)
                messages.success(request, "Подкатегория добавлена.")
            return redirect('dicts_unified')
        if 'edit_subcategory' in request.POST:
            pk = request.POST.get('edit_subcategory')
            name = request.POST.get('subcategory_name')
            category_id = request.POST.get('subcategory_category')
            if pk and name and category_id:
                SubCategory.objects.filter(pk=pk).update(name=name, category_id=category_id)
                messages.success(request, "Подкатегория изменена.")
            return redirect('dicts_unified')

    context = {
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.select_related('type').all(),
        'subcategories': SubCategory.objects.select_related('category').all(),
    }
    return render(request, 'dds/dicts_unified.html', context)

def get_categories(request):
    type_id = request.GET.get('type_id')
    data = []
    if type_id:
        categories = Category.objects.filter(type_id=type_id)
        data = [{'id': c.id, 'name': c.name} for c in categories]
    return JsonResponse({'categories': data})

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    data = []
    if category_id:
        subcategories = SubCategory.objects.filter(category_id=category_id)
        data = [{'id': sc.id, 'name': sc.name} for sc in subcategories]
    return JsonResponse({'subcategories': data})

