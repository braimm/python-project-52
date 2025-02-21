from django.test import TestCase
from django.test import Client
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model


class GetPagesTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.get(pk=1)

    def test_start_page(self):
        path = reverse_lazy('start_page')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_404_error(self):
        response = self.client.get('/nonexistent/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(
            response, template_name='errors/404.html'
        )

    def tearDown(self):
        "Действия после выполнения каждого теста"
