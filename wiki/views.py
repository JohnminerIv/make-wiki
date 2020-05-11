from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from .forms import PageForm
from wiki.models import Page
from django.contrib import messages


class PageListView(ListView):
    """ Renders a list of all Pages. """
    model = Page

    def get(self, request):
        """ GET a list of Pages. """
        pages = self.get_queryset().all()
        return render(request, 'list.html', {
          'pages': pages
        })


class PageCreateView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')

    def get(self, request):
        """ Returns a specific wiki page by slug. """
        context = {
          'form': PageForm(),
        }
        return render(request, 'create.html', context)

    def post(self, request):
        form = PageForm(request.POST)
        if form.is_valid:
            page = form.save(commit=False)
            page.author = request.user
            page.save(update_slug=True)
            messages.success(request, f'{page.title} Created')
            return HttpResponseRedirect(
                reverse('wiki-details-page', args=(page.slug,)))
        # else if form is not valid
        context = {
          'form': form,
        }
        return render(request, 'create.html', context)


class PageDetailView(DetailView):
    """ Renders a specific page based on it's slug."""
    model = Page

    def get(self, request, slug):
        """ Returns a specific wiki page by slug. """
        context = {
          'form': PageForm(),
          'page': self.get_queryset().get(slug__iexact=slug),
        }
        return render(request, 'page.html', context)

    def post(self, request, slug):
        form = PageForm(request.POST)
        if form.is_valid:
            form = form.save(commit=False)
            page = self.get_queryset().get(slug__iexact=slug)
            page.title, page.content = form.title, form.content
            page.save(update_slug=True)
            messages.success(request, f'{page.title} updated')
            return HttpResponseRedirect(
                reverse('wiki-details-page', args=(page.slug,)))
        # else if form is not valid
        context = {
          'form': form,
          'page': self.get_queryset().get(slug__iexact=slug),
        }
        return render(request, 'page.html', context)
