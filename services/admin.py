from django.contrib import admin

from .models import Categories, Products, ProductsExample, HairLength, Masters, Price

# admin.site.register(Categories)
# admin.site.register(Products)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')

@admin.register(ProductsExample)
class ProductsExampleAdmin(admin.ModelAdmin):
    list_display = ('product', 'uploaded_at')
    list_filter = ('product',)
    search_fields = ('product__name',)


@admin.register(HairLength)
class HairLengthAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

# Мастера
@admin.register(Masters)
class MasterAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "discount")
    search_fields = ("name", "level")

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ("product", "get_masters", "hair_length", "min_price", "max_price")
    list_filter = ("product", "masters__level", "hair_length")
    search_fields = ("product__name", "masters__name")
    filter_horizontal = ("masters",) 

    def get_masters(self, obj):
        return ", ".join([str(master) for master in obj.masters.all()])
    get_masters.short_description = "Мастера"
