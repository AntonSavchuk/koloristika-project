from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Categories, Products, ProductsExample, HairLength, Masters, Price

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("name", "category_icon", "category_background")
    fields = ("name", "slug", "svg_image", "preview_icon", "bg_image", "preview_background")
    
    readonly_fields = ("preview_icon", "preview_background")

    def category_icon(self, obj):
        if obj.svg_image:
            return mark_safe(f'<img src="/static/{obj.svg_image}" width="40" height="40">')
        return "Нет иконки"

    def category_background(self, obj):
        if obj.bg_image:
            return mark_safe(f'<img src="{obj.bg_image.url}" width="100">')
        return "Нет фона"

    def preview_icon(self, obj):
        return self.category_icon(obj)

    def preview_background(self, obj):
        return self.category_background(obj)

    category_icon.short_description = "Иконка"
    category_background.short_description = "Фоновое изображение"




@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'category', 'base_price', 'discount', 'show_on_homepage')
    list_filter = ('category', 'base_price', 'discount')
    search_fields = ('name', 'description')
    list_editable = ('base_price', 'discount', 'show_on_homepage')

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
