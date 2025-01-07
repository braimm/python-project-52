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

    # def test_user_update_another_user(self):
    #     self.client.force_login(self.user2)
    #     response = self.client.get(
    #         reverse_lazy('user_update', args=[self.user1.id])
    #     )

    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse_lazy('users'))

    # def test_user_update_post(self):
    #     self.client.force_login(self.user1)
    #     params = self.test_user
    #     response = self.client.post(
    #         reverse_lazy('user_update', args=[self.user1.id]),
    #         data=params
    #     )

    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse_lazy('users'))

    #     updated_user = get_user_model().objects.get(id=self.user1.id)

    #     self.assertEqual(updated_user.username, params['username'])
    #     self.assertEqual(updated_user.first_name, params['first_name'])
    #     self.assertEqual(updated_user.last_name, params['last_name'])

    # def test_user_delete_get(self):
    #     self.client.force_login(self.user1)
    #     response = self.client.get(
    #         reverse_lazy('user_delete', args=[self.user1.id])
    #     )

    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, template_name='delete.html')

    # def test_user_delete_post(self):
    #     self.client.force_login(self.user3)
    #     before_objs_len = len(get_user_model().objects.all())
    #     response = self.client.post(
    #         reverse_lazy('user_delete', args=[self.user3.id])
    #     )
    #     after_objs_len = len(get_user_model().objects.all())

    #     self.assertTrue(after_objs_len == before_objs_len - 1)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse_lazy('users'))
    #     with self.assertRaises(ObjectDoesNotExist):
    #         get_user_model().objects.get(id=self.user3.id)

    # def test_user_delete_linked(self):
    #     self.client.force_login(self.user2)
    #     before_objs_len = len(get_user_model().objects.all())
    #     self.client.post(
    #         reverse_lazy('user_delete', args=[self.user2.id])
    #     )
    #     after_objs_len = len(get_user_model().objects.all())
    #     self.assertTrue(after_objs_len == before_objs_len)
    #     self.assertRaisesMessage(
    #         expected_exception=ProtectedError,
    #         expected_message=''
    #     )
