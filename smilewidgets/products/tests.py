from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ProductPriceTests(APITestCase):
    fixtures = ['0001_fixtures.json', '0002_fixtures.json']

    def setUp(self):
        self.url = reverse('get-price-list')

    def test_get_price_base(self):
        """
        Ensure we can get a price correctly from base parameters.
        """
        data = {'productCode': 'big_widget', 'date':'2019-01-01'}
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, {"product_price": 120000})

    def test_bad_request_base(self):
        """
        Ensure if we pass incorrect parameters we get the appropriate error.
        :return:
        """
        data = {}
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, {"detail": "You must specify a 'date' and 'productCode' via query parameters"})

    def test_get_price_after_switch(self):
        """
        Ensure price changes correctly from base parameters during new event.
        """
        data = {'productCode': 'sm_widget', 'date':'2018-11-24'}
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, {"product_price": 0})

    def test_wrong_product_code(self):
        """
        Ensure if we pass incorrect product code parameters we get the appropriate error.
        :return:
        """
        data = {'productCode': 'blah_widget', 'date':'2019-01-01'}
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, {"detail": "No product price matches those parameters"})

    def test_wrong_gift_card_code(self):
        """
        Ensure if we pass incorrect giftCardCode parameter we get the appropriate error.
        :return:
        """
        data = {'productCode': 'big_widget', 'date':'2019-01-01', 'giftCardCode':'110OFF'}
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, {"detail": "Your gift card code is not valid"})

    def test_get_price_after_gift_card_code(self):
        """
        Ensure price changes correctly after we add a gift card.
        """
        data = {'productCode': 'sm_widget', 'date':'2019-01-01', 'giftCardCode':'10OFF'}
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, {"product_price": 11500})

    def test_fix_zero_price_after_gift_card_code_negative_price(self):
        """
        Ensure price changes correctly after we add a gift card.
        """
        data = {'productCode': 'sm_widget', 'date':'2018-11-24', 'giftCardCode':'10OFF'}
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, {"product_price": 0})