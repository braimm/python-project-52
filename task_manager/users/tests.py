from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.deletion import ProtectedError
# Create your tests here.

class UsersTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']
    # test_user = {
    #     'first_name': 'firstname test input user',
    #     'last_name': 'lastname test input user',
    #     'username': 'inputusername',
    #     'password': '123',
    #     'password2': '123',
    # }

    def setUp(self):
        self.client = Client()
        self.user1 = get_user_model().objects.get(pk=1)
        self.user2 = get_user_model().objects.get(pk=2)
        self.user3 = get_user_model().objects.get(pk=3)
        self.user4 = get_user_model().objects.get(pk=4)

    def test_users_list(self):
        response = self.client.get(reverse_lazy('list_users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='list_users.html')        
        users_list = response.context['users']
        self.assertTrue(len(users_list) == 4)
        self.assertEqual(users_list[0].username, 'user1')
        self.assertEqual(users_list[1].username, 'user2')
        self.assertEqual(users_list[2].username, 'user3')
        self.assertEqual(users_list[3].username, 'free')

    def test_user_create(self):
        response = self.client.get(reverse_lazy('create_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='create_user.html')

        inputform = {
        'first_name': 'firstname test input user',
        'last_name': 'lastname test input user',
        'username': 'inputusername',
        'password': 'Qqq123',
        'password2': 'Qqq123',
        }
        response_post = self.client.post(reverse_lazy('create_user'), inputform)
        self.assertTrue(get_user_model().objects.get(id=5))
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, reverse_lazy('login'))

    def test_another_user_update(self):
        self.client.force_login(self.user2)
        response_redirect = self.client.get(
            reverse_lazy('update_user', args=[self.user1.id])
        )
        self.assertEqual(response_redirect.status_code, 302)
        self.assertRedirects(response_redirect, reverse_lazy('list_users'))

    def test_user_update_without_auth(self):
        response_redirect = self.client.get(
            reverse_lazy('user_update', args=[self.user1.id])
        )
        self.assertEqual(response_redirect.status_code, 302)
        self.assertRedirects(response_redirect, reverse_lazy('login'))

    def test_user_update(self):
        self.client.force_login(self.user1)
        response = self.client.get(
            reverse_lazy('update_user', args=[self.user1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='update_user.html')

