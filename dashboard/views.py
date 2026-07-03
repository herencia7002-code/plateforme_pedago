from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def home(request):
    # Simple dashboard overview — extend with stats as needed
    stats = {
        'users_count': request.user.__class__.objects.count(),
    }
    return render(request, 'dashboard/home.html', {'stats': stats})
