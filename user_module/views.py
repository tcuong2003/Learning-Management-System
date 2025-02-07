from django.shortcuts import render, get_object_or_404, redirect
from .models import UserModule
from .forms import UserModuleForm
from module_group.models import ModuleGroup

def user_module_list(request):
    module_groups = ModuleGroup.objects.all()
    programs = UserModuleForm.objects.all()
    return render(request, 'user_module_list.html', {
        'programs': programs,
        'module_groups': module_groups,
        })

def user_module_create(request):
    if request.method == 'POST':
        form = UserModuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_module:user_module_list')
    else:
        form = UserModuleForm()
    return render(request, 'user_module_form.html', {'form': form})

def user_module_edit(request, pk):
    user_module = get_object_or_404(UserModule, pk=pk)
    if request.method == 'POST':
        form = UserModuleForm(request.POST, instance=user_module)
        if form.is_valid():
            form.save()
            return redirect('user_module:user_module_list')
    else:
        form = UserModuleForm(instance=user_module)
    return render(request, 'user_module_form.html', {'form': form, 'user_module': user_module})

def user_module_delete(request, pk):
    user_module = get_object_or_404(UserModule, pk=pk)
    if request.method == 'POST':
        user_module.delete()
        return redirect('user_module:user_module_list')
    return render(request, 'user_module_delete.html', {'user_module': user_module})
