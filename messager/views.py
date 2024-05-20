from django.shortcuts import render

from django.views.generic.base import TemplateView

class InboxView(TemplateView):
    """Detail view for Community"""
    template_name = "messager/inbox.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context['latest_articles'] = Article.objects.all()[:5]
        return context