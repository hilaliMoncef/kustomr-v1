from django.test import TestCase
from .models import User
from Customer.models import Customer
from Vendor.models import Vendor


class UserModelTests(TestCase):
    """
    We use this function to test that the model always returns a customer associated with the user
    If multiple customers are associated with the user:
        - If the store parameter is sent with a correct store pk, we return the associated customer
        - We return the whole QuerySet otherwise
    """

    def setUp(self):
        # We create two stores
        self.vendor_user = User.objects.create_user(email='commercant@…', password='top_secret')
        self.vendor_user_2 = User.objects.create_user(email='commercant2@…', password='top_secret')
        self.vendor = Vendor.objects.create(user=self.vendor_user, store_name="store")
        self.vendor_2 = Vendor.objects.create(user=self.vendor_user_2, store_name="store2")

    def test_get_customer_single(self):
        """
        We use this function to test that the model always returns a customer associated with the user 
        when a single customer is associated
        """
        user = User.objects.create_user(email='jacob@…', password='top_secret')
        customer = Customer.objects.create(user=user, store_linked=self.vendor)

        self.assertEqual(user.get_customer(), customer)

    def test_get_customer_multiple(self):
        """
        We use this function to test that the model always returns a customer associated with the user 
        when multiple customers is associated
        """
        user = User.objects.create_user(email='jacob@…', password='top_secret')
        customer = Customer.objects.create(user=user, store_linked=self.vendor)
        customer_2 = Customer.objects.create(user=user, store_linked=self.vendor_2)

        related_customers = user.get_customer().all()
        self.assertEqual(related_customers.count(), 2)
        self.assertIn(customer, related_customers)
        self.assertIn(customer_2, related_customers)

    def test_get_customer_multiple_with_store(self):
        """
        We use this function to test that the model always returns a customer associated with the user 
        when multiple customers is associated
        """
        user = User.objects.create_user(email='jacob@…', password='top_secret')
        customer = Customer.objects.create(user=user, store_linked=self.vendor)
        customer_2 = Customer.objects.create(user=user, store_linked=self.vendor_2)

        self.assertEqual(user.get_customer(store=self.vendor.pk), customer)
        self.assertEqual(user.get_customer(store=self.vendor_2.pk), customer_2)
        