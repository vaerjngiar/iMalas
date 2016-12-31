from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import ContactForm, SignUpForm

from django.http import HttpResponseRedirect
from products.models import Category


class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    sign_up_form_class = SignUpForm
    success_url = '/contact/'

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['sign_up_form'] = SignUpForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        sign_up_form = self.sign_up_form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            #instance.user = request.user
            form.name = form.cleaned_data.get('name')
            form.sender = form.cleaned_data.get('sender')
            instance.save()
            return HttpResponseRedirect('/contact/')

        if sign_up_form.is_valid():
            instance = sign_up_form.save(commit=False)
            sign_up_form.email = sign_up_form.cleaned_data.get('email')
            instance.save()
            return HttpResponseRedirect('/about/')

        return render(request, self.template_name, {'form': form,
                                                    'sign_up_form': sign_up_form,
                                                    })

