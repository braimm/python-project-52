from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.messages import get_messages, constants as message_constants
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.deletion import ProtectedError
from .models import Label
# Create your tests here.

class LabelsTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']
    input_label = {'name': 'new_label'}

    def setUp(self):
        self.client = Client()
        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)
        self.free_label = Label.objects.get(pk=3)
        self.user = get_user_model().objects.get(pk=1)


    def test_labels_list_without_auth(self):
        response = self.client.get(reverse_lazy('list_labels'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/labels/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Вы не авторизованы! Пожалуйста, выполните вход.")
        self.assertEqual(messages[0].level, message_constants.ERROR)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message='Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_labels_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('list_labels'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='list_labels.html')
        labels_list = response.context['labels']
        self.assertTrue(len(labels_list) == 3)

    def test_label_create_without_auth(self):
        response = self.client.get(reverse_lazy('create_label'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/labels/create/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Вы не авторизованы! Пожалуйста, выполните вход.")
        self.assertEqual(messages[0].level, message_constants.ERROR)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message='Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_label_create(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('create_label'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='create_label.html')
        response_post = self.client.post(reverse_lazy('create_label'), self.input_label)
        new_label= Label.objects.get(pk=4)
        self.assertTrue(new_label)
        self.assertEqual(new_label.name, self.input_label['name'])
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, reverse_lazy('list_labels'))
        response = self.client.get(reverse_lazy('list_labels'))
        labels_list = response.context['labels']
        self.assertTrue(len(labels_list) == 4)
   

    def test_label_update_without_auth(self):
        response_redirect = self.client.get(
            reverse_lazy('update_label', args=[self.label1.pk])
        )
        self.assertEqual(response_redirect.status_code, 302)
        self.assertRedirects(response_redirect, '/login/?next=/labels/1/update/')
        messages = list(get_messages(response_redirect.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Вы не авторизованы! Пожалуйста, выполните вход.")
        self.assertEqual(messages[0].level, message_constants.ERROR)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message='Вы не авторизованы! Пожалуйста, выполните вход.'
        )

    def test_label_update_using_exist_name(self):
        pass

    def test_label_update(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse_lazy('update_label', args=[self.label1.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='update_label.html')
        inputform = self.input_label
        response = self.client.post(
            reverse_lazy('update_label', args=[self.label1.pk]),
            inputform
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('list_labels'))
        updated_label = Label.objects.get(pk=self.label1.pk)
        self.assertEqual(updated_label.name, inputform['name'])

    def test_label_delete_without_auth(self):
        response_redirect = self.client.get(
            reverse_lazy('delete_label', args=[self.label1.pk])
        )
        self.assertEqual(response_redirect.status_code, 302)
        self.assertRedirects(response_redirect, '/login/?next=/labels/1/delete/')
        messages = list(get_messages(response_redirect.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Вы не авторизованы! Пожалуйста, выполните вход.")
        self.assertEqual(messages[0].level, message_constants.ERROR)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message='Вы не авторизованы! Пожалуйста, выполните вход.'
        )

    def test_free_label_delete(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse_lazy('delete_label', args=[self.free_label.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='delete_label.html')
        count_labels_before_del = len(Label.objects.all())
        response = self.client.post(
            reverse_lazy('delete_label', args=[self.free_label.pk])
        )
        count_labels_after_del = len(Label.objects.all())
        self.assertTrue(count_labels_after_del == count_labels_before_del - 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('list_labels'))
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(id=self.free_label.pk)

    def test_nonfree_label_delete(self):
        self.client.force_login(self.user)
        count_labels_before_del = len(Label.objects.all())
        self.client.post(
            reverse_lazy('delete_label', args=[self.label2.id])
        )
        count_labels_after_del = len(Label.objects.all())
        self.assertTrue(count_labels_before_del == count_labels_after_del)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message='Невозможно удалить метку, потому что она используется'
        )
