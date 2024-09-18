from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from .forms import CategoryForm
from module_group.models import ModuleGroup

# Category views
def category_list(request):
    module_groups = ModuleGroup.objects.all()
   # modules = Module.objects.all()
    subjects = Category.objects.all()
    return render(request, 'category_list.html', {
        'module_groups': module_groups,
      #  'modules': modules,
        # 'subjects': subjects,
        'module_groups': module_groups
    })

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'category_detail.html', {'category': category})

def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category:category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})

def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category:category_list')
    return render(request, 'category_confirm_delete.html', {'category': category})
