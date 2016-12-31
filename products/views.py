from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import Http404
from django.contrib import messages
from django_filters import FilterSet, CharFilter, NumberFilter

from .mixins import StaffRequiredMixin

from .models import Product, Category, Variation
from .forms import VariationInventoryFormSet, ProductFilterForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wishlist.forms import WishlistAddProductForm


# Create your views here.

class FilterMixin(object):
    filter_class = None
    search_ordering_param = "ordering"


    def get_queryset(self, *args, **kwargs):
        try:
            qs = super(FilterMixin, self).get_queryset(*args, **kwargs)
            return qs
        except:
            raise ImproperlyConfigured("You must have a queryset in order to use the FilterMixin")

    def get_context_data(self, *args, **kwargs):
        context = super(FilterMixin, self).get_context_data(*args, **kwargs)
        qs = self.get_queryset()
        ordering = self.request.GET.get(self.search_ordering_param)
        if ordering:
            qs = qs.order_by(ordering)
        filter_class = self.filter_class
        if filter_class:
            f = filter_class(self.request.GET, queryset=qs)
            context["object_list"] = f
        return context


class ProductFilter(FilterSet):
    title = CharFilter(name='title', lookup_type='icontains', distinct=True)
    category = CharFilter(name='categories__title', lookup_type='icontains', distinct=True)
    category_id = CharFilter(name='categories__id', lookup_type='icontains', distinct=True)
    min_price = NumberFilter(name='variation__price', lookup_type='gte', distinct=True)  # (some_price__gte=somequery)
    max_price = NumberFilter(name='variation__price', lookup_type='lte', distinct=True)

    class Meta:
        model = Product
        fields = [
            'min_price',
            'max_price',
            'category',
            'title',
            'description',
        ]



class CategoryListView(FilterMixin, ListView):
    model = Category
    queryset = Category.objects.all()
    filter_class = ProductFilter

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["filter_form"] = ProductFilterForm(data=self.request.GET or None)
        return context


class CategoryDetailView(DetailView):
    model = Category
    filter_class = ProductFilter

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        product_set = obj.product_set.all()
        default_object_list = obj.default_category.all()
        object_list = (product_set | default_object_list).distinct()
        context['object_list'] = object_list
        context["categories"] = Category.objects.all()
        context["filter_form"] = ProductFilterForm(data=self.request.GET or None)
        # context["num_pages"] = round(self.queryset.count() / self.paginate_by) + 1
        return context


class VariationListView(StaffRequiredMixin, ListView):
    model = Variation
    queryset = Variation.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(VariationListView, self).get_context_data(**kwargs)
        context['formset'] = VariationInventoryFormSet(queryset=self.get_queryset())
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = Variation.objects.all()
        product_pk = self.kwargs.get("pk")
        if product_pk:
            product = get_object_or_404(Product, pk=product_pk)
            queryset = Variation.objects.filter(product=product)
        return queryset

    def post(self, request, *args, **kwargs):
        formset = VariationInventoryFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                if new_item.title:
                    product_pk = self.kwargs.get("pk")
                    product = get_object_or_404(Product, pk=product_pk)
                    new_item.product = product
                    new_item.save()

            messages.success(request, "Your inventory and pricing has been updated.")
            return redirect("object_list")
        raise Http404


class ProductListView(FilterMixin, ListView):
    model = Product
    filter_class = ProductFilter
    paginate_by = 8

    def get_queryset(self, **kwargs):
        qs = super(ProductListView, self).get_queryset(**kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(categories__description__icontains=query)
            )
            try:
                qs2 = self.model.objects.filter(
                    Q(price=query) |
                    Q(sale_price=query)
                )
                qs = (qs | qs2).distinct()
            except:
                pass

        return qs

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)

        object_list = Product.objects.all()
        paginator = Paginator(object_list, self.paginate_by)
        page= self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)

        context['object_list'] = object_list
        context["query"] = self.request.GET.get("q")
        context["filter_form"] = ProductFilterForm(data=self.request.GET or None)
        context["form"] = self.request.GET.get("f")
        context["categories"] = Category.objects.all()
        context['pages'] = paginator.page_range

        return context

import random


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        instance = self.get_object()
        context["related"] = sorted(Product.objects.get_related(instance)[:6], key=lambda x: random.random())
        context["categories"] = Category.objects.all()
        context["wishlist_product_form"] = WishlistAddProductForm
        return context
