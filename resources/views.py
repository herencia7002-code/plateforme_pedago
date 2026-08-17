from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import FileResponse
import hashlib
from settings_app.models import PlatformSettings
from .forms import DocumentForm, CommentForm
from .models import Document,  calculate_file_hash
from categories.models import Matiere, Niveau

@login_required

def document_list(request):
    documents = Document.objects.all()
    context = {'documents': documents,'matieres': Matiere.objects.all(), 'niveaux': Niveau.objects.all(),}
    return render(request, 'resources/document_list.html', context)

@login_required
def document_create(request):
    if request.method == "POST":

        form = DocumentForm(
            request.POST,
            request.FILES
        )
        if form.is_valid():
            document = form.save(commit=False)
            document.auteur = request.user
            if document.file:
                hash_fichier = calculate_file_hash(document.file)
                doublon = Document.objects.filter(file_hash=hash_fichier).exists()
                if doublon:
                    messages.error(request,"Ce document existe déjà sur la plateforme.")
                    return render(request, "dashboard/document_form.html",
                        {"form": form, "action": "Ajouter"}
                    )
                document.file_hash = hash_fichier
            document.save()
            messages.success(request,"Document ajouté avec succès." )
            return redirect("resources:document_list")
        else:
            print(form.errors)
    else:
        form = DocumentForm()
    return render(
        request, "dashboard/document_form.html", {"form": form,"action": "Ajouter"}
    )
@login_required
def document_update(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            nouveau_fichier = form.cleaned_data.get("file")
            if nouveau_fichier:
                sha256 = hashlib.sha256()
                for chunk in nouveau_fichier.chunks():
                    sha256.update(chunk)

                nouveau_hash = sha256.hexdigest()
                nouveau_fichier.seek(0)
                doublon = Document.objects.filter( file_hash=nouveau_hash).exclude(pk=document.pk).exists()
                if doublon:
                    messages.error( request,"Ce fichier existe déjà sur la plateforme. La modification a été refusée.")
                    return redirect("resources:document_update", pk=document.pk) 
                document.file_hash = nouveau_hash
            document = form.save(commit=False)
            document.auteur = request.user
            if nouveau_fichier:
                document.file_hash = nouveau_hash
            form.save()
            messages.success(request, 'Document modifié avec succès.')
            return redirect('resources:document_list')
        else:
            print(form.errors)
    else:
        form = DocumentForm(instance=document)
    return render(request, 'dashboard/document_form.html', {'form': form, 'action': 'Modifier', 'document': document})


@login_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document supprimé avec succès.')
        return redirect('resources:document_list')
    return render(request, 'dashboard/document_confirm_delete.html', {'document': document})

@login_required
def add_comment(request, pk):
    document = get_object_or_404(Document, pk=pk)
    settings_obj = PlatformSettings.get_solo()
    if not settings_obj.autoriser_commentaires:
        messages.error(request, "Les commentaires sont actuellement désactivés.")
        return redirect("resources:document_detail",pk=document.id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.document = document
            comment.auteur = request.user
            comment.save()
    return redirect("resources:document_detail", pk=document.pk)

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
    return render( request,"accounts/user_document_list.html",{"documents": documents} )

