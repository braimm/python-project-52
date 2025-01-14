from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.messages import (
    get_messages,
    constants as message_constants
)
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.deletion import ProtectedError
# Create your tests here.


class UsersTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']
    input_user = {
        'first_name': 'firstname test input user',
        'last_name': 'lastname test input user',
        'username': 'inputusername',
        'password': 'Qqq123',
        'password2': 'Qqq123',
        }

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

        inputform = self.input_user
        response_post = self.client.post(
            reverse_lazy('create_user'),
            inputform
        )
        self.assertTrue(get_user_model().objects.get(pk=5))
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, reverse_lazy('login'))

    def test_user_update_without_auth(self):
        response_redirect = self.client.get(
            reverse_lazy('update_user', args=[self.user1.pk])
        )
        self.assertEqual(response_redirect.status_code, 302)
        self.assertRedirects(
            response_redirect,
            '/login/?next=/users/1/update/'
        )
        messages = list(get_messages(response_redirect.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Вы не авторизованы! Пожалуйста, выполните вход."
        )
        self.assertEqual(messages[0].level, message_constants.ERROR)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message='Вы не авторизованы! Пожалуйста, выполните вход.'
        )

    def test_another_user_update(self):
        self.client.force_login(self.user2)
        response_redirect = self.client.get(
            reverse_lazy('update_user', args=[self.user1.pk])
        )
        self.assertEqual(response_redirect.status_code, 302)
        self.assertRedirects(response_redirect, reverse_lazy('list_users'))
        messages = list(get_messages(response_redirect.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "У вас нет прав для изменения другого пользователя."
        )
        self.assertEqual(messages[0].level, message_constants.ERROR)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message='У вас нет прав для \
                изменения другого пользователя.'
        )

    def test_user_update(self):
        self.client.force_login(self.user1)
        response = self.client.get(
            reverse_lazy('update_user', args=[self.user1.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='update_user.html')
        inputform = self.input_user
        response = self.client.post(
            reverse_lazy('update_user', args=[self.user1.pk]),
            inputform
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('list_users'))
        updated_user = get_user_model().objects.get(pk=self.user1.pk)
        self.assertEqual(updated_user.username, inputform['username'])
        self.assertEqual(updated_user.first_name, inputform['first_name'])
        self.assertEqual(updated_user.last_name, inputform['last_name'])

    def test_user_delete_without_auth(self):
        response_redirect = self.client.get(
            reverse_lazy('delete_user', args=[self.user1.pk])
        )
        self.assertEqual(response_redirect.status_code, 302)
        self.assertRedirects(
            response_redirect,
            '/login/?next=/users/1/delete/'
        )
        messages = list(get_messages(response_redirect.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Вы не авторизованы! Пожалуйста, выполните вход."
        )
        self.assertEqual(messages[0].level, message_constants.ERROR)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message='Вы не авторизованы! \
                Пожалуйста, выполните вход.'
        )

    def test_another_user_delete(self):
        self.client.force_login(self.user2)
        response_redirect = self.client.get(
            reverse_lazy('delete_user', args=[self.user1.pk])
        )
        self.assertEqual(response_redirect.status_code, 302)
        self.assertRedirects(response_redirect, reverse_lazy('list_users'))
        messages = list(get_messages(response_redirect.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "У вас нет прав для изменения другого пользователя."
        )
        self.assertEqual(messages[0].level, message_constants.ERROR)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message='У вас нет прав для изменения \
                другого пользователя.')

    def test_free_user_delete(self):
        self.client.force_login(self.user4)
        response = self.client.get(
            reverse_lazy('delete_user', args=[self.user4.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='delete_user.html')
        count_users_before_del = len(get_user_model().objects.all())
        response = self.client.post(
            reverse_lazy('delete_user', args=[self.user4.pk])
        )
        count_users_after_delete = len(get_user_model().objects.all())
        self.assertTrue(count_users_after_delete == count_users_before_del - 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('list_users'))
        with self.assertRaises(ObjectDoesNotExist):
            get_user_model().objects.get(id=self.user4.pk)

    def test_nonfree_user_delete(self):
        self.client.force_login(self.user1)
        count_users_before_del = len(get_user_model().objects.all())
        self.client.post(
            reverse_lazy('delete_user', args=[self.user1.pk])
        )
        count_users_after_del = len(get_user_model().objects.all())
        self.assertTrue(count_users_before_del == count_users_after_del)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message='Невозможно удалить пользователя, \
                потому что он используется'
        )
