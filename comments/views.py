from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

from resources.models import Comment


class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = "comments/comment_list.html"
    context_object_name = "comments"
    paginate_by = 10

    def get_queryset(self):
        queryset = Comment.objects.select_related(
            "auteur",
            "document"
        ).order_by("-created_at")

        q = self.request.GET.get("q")

        if q:
            queryset = queryset.filter(
                Q(content__icontains=q) |
                Q(user__username__icontains=q) |
                Q(document__title__icontains=q)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["nb_comments"] = Comment.objects.count()
        context["recherche"] = self.request.GET.get("q", "")

        return context

def commentaires(request):
    aujourd_hui = timezone.now().date()
    debut_semaine = aujourd_hui - timedelta(days=aujourd_hui.weekday())

    derniers_commentaires = (
        Comment.objects.select_related("user", "document")
        .order_by("-created_at")[:10]
    )

    context = {
        "nb_commentaires": Comment.objects.count(),

        "commentaires_aujourdhui": Comment.objects.filter(
            created_at__date=aujourd_hui
        ).count(),

        "commentaires_semaine": Comment.objects.filter(
            created_at__date__gte=debut_semaine
        ).count(),

        "derniers_commentaires": derniers_commentaires,
    }

    return render(
        request,
        "dashboard/commentaires.html",
        context,
    )
class CommentDetailView(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = "comments/comment_detail.html"
    context_object_name = "comment"


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "comments/comment_confirm_delete.html"
    success_url = reverse_lazy("comments:comment_list")

