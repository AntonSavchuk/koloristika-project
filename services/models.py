from django.db import models


class Categories(models.Model):
    name = models.CharField(
        max_length=150, unique=True, verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=200, verbose_name='URL', unique=True, null=True, blank=True
    )
    svg_image = models.FileField(
        upload_to='svg_images', blank=True, null=True, verbose_name='Фото'
    )
    short_description = models.TextField(
        blank=True, null=True, verbose_name='Краткое описание'
    )

    class Meta:
        db_table = 'category'
        verbose_name = 'категорию'
        verbose_name_plural = 'категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Masters(models.Model):
    name = models.CharField(
        max_length=150, verbose_name='ФИО мастера'
    )
    level = models.CharField(
        max_length=100, verbose_name='Уровень мастера'
    )
    photo = models.ImageField(
        upload_to='masters/', blank=True, null=True, verbose_name='Фото мастера'
    )
    description = models.TextField(
        blank=True, null=True, verbose_name='Описание мастера'
    )
    discount = models.DecimalField(
        default=0.00, max_digits=5, decimal_places=2, verbose_name='Скидка в %'
    )

    class Meta:
        db_table = 'master'
        verbose_name = 'мастера'
        verbose_name_plural = 'мастера'
        ordering = ['level', 'name']

    def __str__(self):
        return f"{self.level} {self.name}"


class HairLength(models.Model):
    name = models.CharField(
        max_length=50, unique=True, verbose_name='Длина волос'
    )

    class Meta:
        db_table = "hair_length"
        verbose_name = "длину волос"
        verbose_name_plural = "длины волос"
        ordering = ['name']

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(
        max_length=150, unique=True, verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=200, verbose_name='URL', unique=True, blank=True, null=True
    )
    description = models.TextField(
        blank=True, null=True, verbose_name='Описание товара'
    )
    image = models.ImageField(
        upload_to='services_images', blank=True, null=True, verbose_name='Фото'
    )
    discount = models.DecimalField(
        default=0.00, max_digits=5, decimal_places=2, verbose_name='Скидка в %'
    )
    category = models.ForeignKey(
        to=Categories, on_delete=models.CASCADE, verbose_name='Категория'
    )
    base_price = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Фиксированная цена"
    )
    show_on_homepage = models.BooleanField(
        default=False, verbose_name="Показывать на главной"
    )
                                    
    class Meta:
        db_table = 'product'
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name']


    def __str__(self):
        return self.name
    

class ProductsExample(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name='examples', verbose_name='Продукт'
    )
    image = models.ImageField(
        upload_to='product_examples/', verbose_name='Фото примера работы'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата загрузки'
    )
    
    class Meta:
        db_table = 'product_example'
        verbose_name = 'пример работы'
        verbose_name_plural = 'примеры работ'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f'Пример для {self.product.name}'
    

class Price(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="prices", verbose_name="Продукт"
    )
    masters = models.ManyToManyField(
        Masters, related_name="prices", verbose_name="Мастер", blank=True
    )
    hair_length = models.ForeignKey(
        HairLength, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Длина волос"
    )
    min_price = models.IntegerField(
        verbose_name="Минимальная цена"
    )
    max_price = models.IntegerField(
        blank=True, null=True, verbose_name="Максимальная цена"
    )

    class Meta:
        db_table = "product_price"
        verbose_name = "цену"
        verbose_name_plural = "цены"
        ordering = ['product__name', 'min_price']

    def __str__(self):
        return f"{self.product.name} ({self.hair_length or 'Без длины'}) - {self.min_price} ₽ - {self.max_price} ₽"
