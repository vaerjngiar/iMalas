from django.contrib import admin

# Register your models here.


from .models import Product, Variation, ProductImage, Category


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 10


class VariationInline(admin.TabularInline):
    model = Variation
    extra = 0
    max_num = 10


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price']
    inlines = [
        ProductImageInline,
        VariationInline,
    ]

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)

# admin.site.register(Variation)

admin.site.register(ProductImage)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'description', 'active']
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Category, CategoryAdmin)


