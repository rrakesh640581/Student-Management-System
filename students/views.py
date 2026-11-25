
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Student
from .forms import StudentForm


# View all students
@login_required
def student_list(request):
    query = request.GET.get('search', '').strip()
    course = request.GET.get('course', '').strip()

    students = Student.objects.filter(user=request.user)

    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query)
        )

    if course:
        students = students.filter(course__iexact=course)

    context = {
        'students': students,
        'query': query,
        'selected_course': course
    }

    return render(request, 'students/student_list.html', context)


# Add new student
@login_required
def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()

            return redirect('student_list')
    else:
        form = StudentForm()

    return render(
        request,
        'students/student_form.html',
        {'form': form, 'title': 'Add Student'}
    )


# Edit student
@login_required
def student_edit(request, pk):
    student = get_object_or_404(
        Student,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)

    return render(
        request,
        'students/student_form.html',
        {'form': form, 'title': 'Edit Student'}
    )


# Delete student
@login_required
def student_delete(request, pk):
    student = get_object_or_404(
        Student,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        student.delete()
        return redirect('student_list')

    return render(
        request,
        'students/student_confirm_delete.html',
        {'student': student}
    )


# Dashboard
@login_required
def dashboard(request):
    user_students = Student.objects.filter(user=request.user)

    total_students = user_students.count()

    python_students = user_students.filter(
        course__iexact='Python'
    ).count()

    java_students = user_students.filter(
        course__iexact='Java'
    ).count()

    other_students = total_students - python_students - java_students

    total_courses = user_students.values('course').distinct().count()

    recent_students = user_students.order_by('-id')[:5]

    context = {
        'total_students': total_students,
        'python_students': python_students,
        'java_students': java_students,
        'other_students': other_students,
        'total_courses': total_courses,
        'recent_students': recent_students,
    }

    return render(request, 'students/dashboard.html', context)


# Student details
@login_required
def student_detail(request, id):
    student = get_object_or_404(
        Student,
        id=id,
        user=request.user
    )

    return render(
        request,
        'students/student_detail.html',
        {'student': student}
    )


# User registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_list')
    else:
        form = UserCreationForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )
