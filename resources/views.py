from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import FileResponse

from .forms import DocumentForm, CommentForm
from .models import Document
from categories.models import Matiere, Niveau

@login_required
def document_list(request):
    documents = Document.objects.all()
    context = {'documents': documents,'matieres': Matiere.objects.all(), 'niveaux': Niveau.objects.all(),}
    return render(request, 'resources/document_list.html', context)

@login_required
def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.auteur = request.user
            document.save()
            messages.success(request, 'Document ajouté avec succès.')
            return redirect('resources:document_list')
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
            return redirect('resources:document_list')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'resources/document_form.html', {'form': form, 'action': 'Modifier', 'document': document})


@login_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document supprimé avec succès.')
        return redirect('resources:document_list')
    return render(request, 'resources/document_confirm_delete.html', {'document': document})

@login_required
def add_comment(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.document = document
            comment.auteur = request.user
            comment.save()
    return redirect("resources:document_detail", pk=document.pk)

@login_required
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    form = CommentForm()
    return render(request, "resources/document_detail.html", { "document": document, "form": form, },)


@login_required
def download_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    document.incrementer_telechargements()
    return FileResponse( document.file.open(), as_attachment=True, filename=document.file.name.split('/')[-1])


@login_required
def user_document_list(request):
    documents = Document.objects.filter(status='approved')
    return render( request,"resources/user_document_list.html",{"documents": documents} )

