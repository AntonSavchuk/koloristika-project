from collections import defaultdict

from django.shortcuts import render, get_object_or_404
from django.db.models import Min, Max
from .models import Categories, Products, ProductsExample, Price, Masters

def product_price(request):
    categories = Categories.objects.all()

    master_levels = Masters.objects.values_list("level", flat=True).distinct()

    category_slug = request.GET.get("category", "all")
    price_min = request.GET.get("price_min")
    price_max = request.GET.get("price_max")
    master_type = request.GET.get("master")

    price_min = int(price_min) if price_min and price_min.isdigit() else None
    price_max = int(price_max) if price_max and price_max.isdigit() else None

    products = Products.objects.all()

    if category_slug != "all":
        products = products.filter(category__slug=category_slug)

    if master_type and master_type != "all":
        filtered_prices = Price.objects.filter(masters__level__iexact=master_type)
        products = products.filter(prices__in=filtered_prices).distinct()

    product_list = []
    for product in products:
        is_fixed_price = False 
        final_min_price = None
        final_max_price = None

        if product.base_price:
            is_fixed_price = True
            final_min_price = product.base_price
            final_max_price = product.base_price

            if product.discount and product.discount > 0:
                final_min_price -= (final_min_price * product.discount // 100)

        if not is_fixed_price:
            if master_type and master_type != "all":
                price_data = product.prices.filter(masters__level__iexact=master_type).aggregate(
                    min_price=Min("min_price"),
                    max_price=Max("max_price")
                )
            else:
                price_data = product.prices.aggregate(
                    min_price=Min("min_price"),
                    max_price=Max("max_price")
                )

            min_price_db = price_data["min_price"]
            max_price_db = price_data["max_price"]

            if min_price_db:
                final_min_price = min_price_db
            if max_price_db:
                final_max_price = max_price_db

        if final_max_price is None:
            final_max_price = final_min_price

        if price_min is not None and final_min_price is not None:
            if final_min_price < price_min:
                continue  

        if price_max is not None and final_max_price is not None:
            if final_max_price > price_max:
                continue 

        product_list.append({
            "product": product,
            "min_price": final_min_price,
            "max_price": final_max_price,
            "is_fixed_price": is_fixed_price
        })

    context = {
        "products": product_list,
        "categories": categories,
        "master_levels": master_levels,
        "selected_category": category_slug,
        "selected_master": master_type,
        "selected_price_min": price_min if price_min is not None else "",
        "selected_price_max": price_max if price_max is not None else "",
    }
    return render(request, "services/price.html", context)


def services(request):

    categories = Categories.objects.all()

    context = {
        "title": "KOLORISTIKA - Услуги",
        "categories": categories,
    }

    return render(request, 'services/services.html', context)


def service_detail(request, slug):

    category = get_object_or_404(Categories, slug=slug)
    products = Products.objects.filter(category=category)

    context = {
        "title": f"KOLORISTIKA - {category}",
        "category": category,
        "products": products,
    }

    return render(request, 'services/service.html', context)


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Products, slug=product_slug, category__slug=category_slug)
    prices = Price.objects.filter(product=product).prefetch_related("masters", "hair_length")
    examples = ProductsExample.objects.filter(product=product)

    price_data = defaultdict(list)

    # Проверяем, есть ли базовая цена у продукта (фиксированная без мастера)
    if product.base_price:
        base_discount_price = product.base_price
        if product.discount and product.discount > 0:
            base_discount_price -= (base_discount_price * product.discount // 100)

        price_data[None].append({
            "master": None,
            "hair_length": None,
            "min_price": product.base_price,
            "max_price": None,
            "discount_min": base_discount_price,
            "discount_max": None,
        })

    # Группируем цены по длине волос
    for price in prices:
        length_key = price.hair_length.name if price.hair_length else "Фиксированная цена"
        
        for master in price.masters.all():
            min_price = price.min_price
            max_price = price.max_price if price.max_price else None

            discount_min_price = min_price
            discount_max_price = max_price

            if master.discount and master.discount > 0:
                discount_min_price -= (discount_min_price * master.discount // 100)
                if discount_max_price:
                    discount_max_price -= (discount_max_price * master.discount // 100)
            elif product.discount and product.discount > 0:
                discount_min_price -= (discount_min_price * product.discount // 100)
                if discount_max_price:
                    discount_max_price -= (discount_max_price * product.discount // 100)

            price_data[length_key].append({
                "master": master,
                "hair_length": price.hair_length,
                "min_price": min_price,
                "max_price": max_price,
                "discount_min": discount_min_price if discount_min_price != min_price else None,
                "discount_max": discount_max_price if discount_max_price and discount_max_price != max_price else None,
            })

    print(price_data)  # Отладочный вывод для проверки данных

    context = {
        "title": f"KOLORISTIKA - {product.name}",
        "product": product,
        "examples": examples,
        "prices": dict(price_data),  # Преобразуем defaultdict в обычный dict
    }

    return render(request, "services/product.html", context)
