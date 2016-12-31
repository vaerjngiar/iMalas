from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View, FormView
from django.views.generic.detail import DetailView
from products.models import Product, Category
from about.forms import SignUpForm
from django.http import HttpResponseRedirect
import random


class HomeView(FormView, ListView):
    model = Product
    template_name = 'home/home.html'
    form_class = SignUpForm

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['object_list'] = sorted(Product.objects.all(), key = lambda x: random.random())[:6]
        context['new_list'] = sorted(Product.objects.filter(new=True), key = lambda x: random.random())[:6]
        context['categories'] = Category.objects.all()
        #context['products'] = sorted(Product.objects.all()[:6], key= lambda x: random.random())
        return context

    def post(self, request, *args, **kwargs):
        sign_up_form = self.form_class(request.POST)
        if sign_up_form.is_valid():
            instance = sign_up_form.save(commit=False)
            sign_up_form.email = sign_up_form.cleaned_data.get('email')
            instance.save()
            return HttpResponseRedirect('/about/')

        return render(request, self.template_name, {'sign_up_form': sign_up_form, })