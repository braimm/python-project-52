from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.messages import (
    get_messages,
    constants as message_constants
)
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.deletion import ProtectedError
from .models import Status
# Create your tests here.


class StatusesTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']
    input_status = {'name': 'new_status'}

    def setUp(self):
        self.client = Client()
        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)
        self.free_status = Status.objects.get(pk=3)
        self.user = get_user_model().objects.get(pk=1)

    def test_statuses_list_without_auth(self):
        response = self.client.get(reverse_lazy('list_statuses'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/statuses/')
        messages = list(get_messages(response.wsgi_request))
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

    def test_statuses_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('list_statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='list_statuses.html')
        labels_list = response.context['statuses']
        self.assertTrue(len(labels_list) == 3)

    def test_status_create_without_auth(self):
        response = self.client.get(reverse_lazy('create_status'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/statuses/create/')
        messages = list(get_messages(response.wsgi_request))
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

    def test_status_create(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('create_status'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='create_status.html')
        response_post = self.client.post(
            reverse_lazy('create_status'),
            self.input_status
        )
        new_status = Status.objects.get(pk=4)
        self.assertTrue(new_status)
        self.assertEqual(new_status.name, self.input_status['name'])
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, reverse_lazy('list_statuses'))
        response = self.client.get(reverse_lazy('list_statuses'))
        statuses_list = response.context['statuses']
        self.assertTrue(len(statuses_list) == 4)

    def test_status_update_without_auth(self):
        response_redirect = self.client.get(
            reverse_lazy('update_status', args=[self.status1.pk])
        )
        self.assertEqual(response_redirect.status_code, 302)
        self.assertRedirects(
            response_redirect,
            '/login/?next=/statuses/1/update/'
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

    def test_status_update_using_exist_name(self):
        pass

    def test_status_update(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse_lazy('update_status', args=[self.status1.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='update_status.html')
        inputform = self.input_status
        response = self.client.post(
            reverse_lazy('update_status', args=[self.status1.pk]),
            inputform
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('list_statuses'))
        updated_status = Status.objects.get(pk=self.status1.pk)
        self.assertEqual(updated_status.name, inputform['name'])

    def test_status_delete_without_auth(self):
        response_redirect = self.client.get(
            reverse_lazy('delete_status', args=[self.status1.pk])
        )
        self.assertEqual(response_redirect.status_code, 302)
        self.assertRedirects(
            response_redirect,
            '/login/?next=/statuses/1/delete/'
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

    def test_nonfree_status_delete(self):
        self.client.force_login(self.user)
        count_statuses_before_del = len(Status.objects.all())
        self.client.post(
            reverse_lazy('delete_status', args=[self.status2.pk])
        )
        count_statuses_after_del = len(Status.objects.all())
        self.assertTrue(count_statuses_before_del == count_statuses_after_del)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message='Невозможно удалить метку, \
                потому что она используется'
        )

    def test_free_status_delete(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse_lazy('delete_status', args=[self.free_status.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='delete_status.html')
        count_statuses_before_del = len(Status.objects.all())
        response = self.client.post(
            reverse_lazy('delete_status', args=[self.free_status.pk])
        )
        count_statuses_after_del = len(Status.objects.all())
        self.assertTrue(
            count_statuses_after_del == count_statuses_before_del - 1
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('list_statuses'))
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(pk=self.free_status.pk)
