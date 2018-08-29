from django.db.models import Q

from rest_framework.exceptions import NotFound, ParseError
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import routers

from .models import ProductPrice, GiftCard


router = routers.DefaultRouter()


class ProductPriceViewSet(GenericViewSet):
    queryset = ProductPrice.objects.none()
    throttle_scope = 'anon'

    def list(self, request):
        params = request.GET

        product_code = params.get('productCode')
        date = params.get('date')
        gift_card_code = params.get('giftCardCode')

        if not product_code or not date:
            raise ParseError("You must specify a 'date' and 'productCode' via query parameters")

        # assumption is closest start_date to date added takes priority in case of collisions
        product_price = ProductPrice.objects.filter(product__code=product_code,date_start__lte=date)
        product_price = product_price.filter(Q(date_end__gte=date)|Q(date_end__isnull=True))
        product_price = product_price.order_by('-date_start')
        product_price = product_price.first()

        if product_price is None:
            raise NotFound("No product price matches those parameters", code=404)

        final_price = product_price.price  # In cents

        if gift_card_code:
            try:
                gift_card = GiftCard.objects.get(
                    Q(date_end__gte=date) | Q(date_end__isnull=True),
                    code=gift_card_code,
                    date_start__lte=date,
                )
                gift_card_value = gift_card.amount  # In cents
                if gift_card_value > 0:
                    final_price = final_price - gift_card_value
                    final_price = 0 if final_price < 0 else final_price  # Ignore negative balances and return 0 cost
            except:
                raise ParseError("Your gift card code is not valid")

        return Response({"product_price": final_price})

router.register(r'get-price', ProductPriceViewSet, base_name='get-price')

