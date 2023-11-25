from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager

ORDER_STATUS = (
    ("oo", "В обработке"),
    ("oo", "Сборка"),
    ("delivery", "Отправлен"),
    ("close", "Закрыт"),
    ("canceled", "Отменён")
)

USER_TYPE = (
    ("shop", "Магазин"),
    ("buyer", "Покупатель")
)


class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = User(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        assert extra_fields['is_staff']
        assert extra_fields['is_superuser']
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(verbose_name="email",
                              null=False,
                              unique=True)
    type = models.CharField(verbose_name="Тип пользователя",
                            choices=USER_TYPE,
                            max_length=10)
    address = models.CharField(verbose_name="Адрес")

    REQUIRED_FIELDS = ["type"]
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Информация о пользователе"
        verbose_name_plural = "Информация о пользователях"

    def __str__(self):
        return f'{self.username} - {self.type}'


class Shop(models.Model):
    name = models.CharField(verbose_name="Название",
                            null=False,
                            unique=True)
    url = models.URLField(verbose_name="Сайт",
                          null=True,
                          unique=True)
    user = models.ForeignKey(User,
                             verbose_name="Пользователь",
                             on_delete=models.CASCADE)
    accept_orders = models.BooleanField(verbose_name="принимает заказы",
                                        default=True)

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

    def __str__(self):
        return self.name


class Category(models.Model):
    shops = models.ManyToManyField(Shop,
                                   verbose_name="Магазины")
    name = models.CharField(verbose_name="Наименование",
                            null=False,
                            unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 verbose_name="Категория",
                                 on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название",
                            null=False)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    product = models.ForeignKey(Product,
                                verbose_name="Продукт",
                                on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop,
                             verbose_name="Магазин",
                             on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название",
                            null=False)
    quantity = models.IntegerField(verbose_name="Количество",
                                   null=False)
    price = models.FloatField(verbose_name="Цена",
                              null=False)
    price_rrc = models.FloatField(verbose_name="Рекомендованная розничная цена",
                                  null=False)

    class Meta:
        verbose_name = "Информация о продукте"
        verbose_name_plural = "Информация о продуктах"

    def __str__(self):
        return self.name


class Parameter(models.Model):
    name = models.CharField(verbose_name="Наименование",
                            null=False,
                            unique=True)

    class Meta:
        verbose_name = "Параметр"
        verbose_name_plural = "Параметры"

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo,
                                     verbose_name="Продукт",
                                     on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter,
                                  verbose_name="Параметр",
                                  on_delete=models.CASCADE)
    value = models.CharField(verbose_name="Значение",
                             null=False)

    class Meta:
        verbose_name = "Параметр продукта"
        verbose_name_plural = "Парметры продукта"

    def __str__(self):
        return self.parameter.name


class Order(models.Model):
    user = models.ForeignKey(User,
                             verbose_name="Пользователь",
                             on_delete=models.CASCADE)
    dt = models.DateTimeField(verbose_name="Дата и время")
    status = models.CharField(verbose_name="Статус",
                              choices=ORDER_STATUS)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return self.status


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              verbose_name="Заказ",
                              on_delete=models.CASCADE)
    product = models.ForeignKey(ProductInfo,
                                verbose_name="Продукт",
                                on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop,
                             verbose_name="Магазин",
                             on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Количество",
                                   null=False)

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return self.product.name


