from django.test import TestCase
from django.test import Client
from django.urls import reverse_lazy


class GetPagesTestCase(TestCase):
    fixtures = []

    def setUp(self):
        self.client = Client()
        "Инициализация перед выполнением каждого теста"

    def test_start_page(self):
        path = reverse_lazy('start_page')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_login(self):
        response = self.client.post(
            reverse_lazy("login"),
            {"username": "123", "password": "123"}
        )
        response.status_code

    def tearDown(self):
        "Действия после выполнения каждого теста"
