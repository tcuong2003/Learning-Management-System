from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Role
from .forms import UserForm, RoleForm

# User views
# def user_list(request):
#     users = User.objects.all()
#     return render(request, 'user_list.html', {'users': users})

# TEST1----------------------------------------------------------------
import pandas as pd
import bcrypt
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Role
from .forms import UserForm, RoleForm, ExcelImportForm

def user_list(request):
    users = User.objects.all()
    if request.method == 'POST':
        form = ExcelImportForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['excel_file']
            try:
                df = pd.read_excel(uploaded_file)
                for index, row in df.iterrows():
                    username = row["username"]
                    password = str(row["password"])
                    email = row["email"]
                    full_name = row["full_name"]
                    role_id = row["role_id"]

                    role_name = get_role_quick_and_dirty_way(role_id)
                    if role_name == "Unknown role":
                        messages.error(request, f"Invalid role '{role_name}' for user '{username}'. Skipping.")
                        continue

                    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

                    insert_user(username, hashed_password, email, full_name, role_id)

                messages.success(request, "Users imported successfully!")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
            return redirect('user:user_list')
    else:
        form = ExcelImportForm()

    return render(request, 'user_list.html', {'users': users, 'form': form})

def get_role_quick_and_dirty_way(role_id):
    roles = {
        1: "student",
        2: "teacher",
        3: "admin",
        4: "super admin"
    }
    return roles.get(role_id, "Unknown role")

def insert_user(username, hashed_password, email, full_name, role_id):
    try:
        User.objects.create(
            username=username,
            password=hashed_password.decode('utf-8'),
            email=email,
            full_name=full_name,
            role_id=role_id
        )
        return True, None
    except Exception as e:
        return False, str(e)


def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'user_detail.html', {'user': user})

def user_add(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:user_list')
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form})

def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user:user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_form.html', {'form': form})





