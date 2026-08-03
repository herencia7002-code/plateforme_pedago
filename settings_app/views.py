from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .models import PlatformSettings
from .forms import PlatformSettingsForm

@staff_member_required
def parametres_generaux(request):
    settings_obj = PlatformSettings.get_solo()

    if request.method == "POST":
        form = PlatformSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Modifications enregistrées avec succès.")
            return redirect("parametres_generaux")
    else:
        form = PlatformSettingsForm(instance=settings_obj)

    return render(request, "settings_app/parametres.html", {"form": form})