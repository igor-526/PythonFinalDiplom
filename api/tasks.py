import yaml
from pprint import pprint
from api.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


def partner_update(file, user):
    data = yaml.safe_load(file)
    try:
        shop = Shop.objects.get_or_create(
            name=data['shop'],
            user=user
        )
        for category in data['categories']:
            cat = Category.objects.get_or_create(
                id=category['id'],
                name=category['name'],
            )
            cat[0].shops.add(shop[0])
        for product in data['goods']:
            prod = Product.objects.get_or_create(
                id=product['id'],
                name=product['model'],
                category=Category.objects.get(id=product['category'])
            )
            prodinfo = ProductInfo.objects.get_or_create(
                product=prod[0],
                shop=shop[0],
                name=product['name'],
                price=product['price'],
                price_rrc=product['price_rrc'],
                quantity=product['quantity']
            )
            for parameter in product['parameters']:
                param = Parameter.objects.get_or_create(
                    name=parameter
                )
                ProductParameter.objects.get_or_create(
                    product_info=prodinfo[0],
                    parameter=param[0],
                    value=product['parameters'][parameter]
                )
        return {"status": "success"}
    except Exception as ex:
        return {"status": f"error: {ex}"}

