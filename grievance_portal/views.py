import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Grievance, Department, GrievanceCategory, GrievanceResponse
from .forms import GrievanceForm, GrievanceResponseForm, GrievanceStatusForm, UserRegistrationForm

def home(request):
    departments = Department.objects.all()
    return render(request, 'home.html', {'departments': departments})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def submit_grievance(request):
    if request.method == 'POST':
        form = GrievanceForm(request.POST, request.FILES)
        if form.is_valid():
            grievance = form.save(commit=False)
            grievance.user = request.user
            grievance.reference_id = f"GR-{uuid.uuid4().hex[:8].upper()}"
            grievance.save()
            messages.success(request, f'Grievance submitted successfully. Your reference ID is {grievance.reference_id}')
            return redirect('my_grievances')
    else:
        form = GrievanceForm()
    
    categories = GrievanceCategory.objects.all()
    return render(request, 'submit_grievance.html', {'form': form, 'categories': categories})

@login_required
def my_grievances(request):
    grievances = Grievance.objects.filter(user=request.user).order_by('-created_at')
    
    search_query = request.GET.get('search', '')
    if search_query:
        grievances = grievances.filter(
            Q(title__icontains=search_query) | 
            Q(reference_id__icontains=search_query)
        )
    
    paginator = Paginator(grievances, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'my_grievances.html', {'page_obj': page_obj, 'search_query': search_query})

@login_required
def grievance_detail(request, reference_id):
    grievance = get_object_or_404(Grievance, reference_id=reference_id)
    
    # Check if the user is the owner or staff
    if grievance.user != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to view this grievance.")
        return redirect('my_grievances')
    
    responses = grievance.responses.all().order_by('created_at')
    
    # Handle new response submission
    if request.method == 'POST':
        form = GrievanceResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.grievance = grievance
            response.responder = request.user
            response.save()
            messages.success(request, 'Response added successfully.')
            return redirect('grievance_detail', reference_id=reference_id)
    else:
        form = GrievanceResponseForm()
    
    return render(request, 'grievance_detail.html', {
        'grievance': grievance,
        'responses': responses,
        'form': form
    })

@staff_member_required
def admin_dashboard(request):
    total_grievances = Grievance.objects.count()
    pending = Grievance.objects.filter(status='pending').count()
    in_progress = Grievance.objects.filter(status='in_progress').count()
    resolved = Grievance.objects.filter(status='resolved').count()
    rejected = Grievance.objects.filter(status='rejected').count()
    
    return render(request, 'admin/dashboard.html', {
        'total_grievances': total_grievances,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved,
        'rejected': rejected
    })

@staff_member_required
def admin_grievance_list(request):
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    grievances = Grievance.objects.all().order_by('-created_at')
    
    if status_filter:
        grievances = grievances.filter(status=status_filter)
    
    if search_query:
        grievances = grievances.filter(
            Q(title__icontains=search_query) | 
            Q(reference_id__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )
    
    paginator = Paginator(grievances, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin/grievance_list.html', {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'search_query': search_query
    })

@staff_member_required
def admin_grievance_detail(request, reference_id):
    grievance = get_object_or_404(Grievance, reference_id=reference_id)
    responses = grievance.responses.all().order_by('created_at')
    
    # Handle status update
    if request.method == 'POST' and 'update_status' in request.POST:
        status_form = GrievanceStatusForm(request.POST, instance=grievance)
        if status_form.is_valid():
            status_form.save()
            messages.success(request, 'Status updated successfully.')
            return redirect('admin_grievance_detail', reference_id=reference_id)
    else:
        status_form = GrievanceStatusForm(instance=grievance)
    
    # Handle new response
    if request.method == 'POST' and 'add_response' in request.POST:
        response_form = GrievanceResponseForm(request.POST)
        if response_form.is_valid():
            response = response_form.save(commit=False)
            response.grievance = grievance
            response.responder = request.user
            response.save()
            messages.success(request, 'Response added successfully.')
            return redirect('admin_grievance_detail', reference_id=reference_id)
    else:
        response_form = GrievanceResponseForm()
    
    return render(request, 'admin/grievance_detail.html', {
        'grievance': grievance,
        'responses': responses,
        'status_form': status_form,
        'response_form': response_form
    })