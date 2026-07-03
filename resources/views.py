from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DocumentForm
from .models import Document


@login_required
def document_list(request):
    documents = Document.objects.all()
    return render(request, 'resources/document_list.html', {'documents': documents})


@login_required
def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            messages.success(request, 'Document ajouté avec succès.')
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'resources/document_form.html', {'form': form, 'action': 'Ajouter'})


@login_required
def document_update(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document modifié avec succès.')
            return redirect('document_list')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'resources/document_form.html', {'form': form, 'action': 'Modifier', 'document': document})


@login_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document supprimé avec succès.')
        return redirect('document_list')
    return render(request, 'resources/document_confirm_delete.html', {'document': document})
