from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.messages import (
    get_messages,
    constants as message_constants
)
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.deletion import ProtectedError
from .models import Task

# Create your tests here.


class TaskTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']
    input_task = {
            "name": "new_task",
            "description": "Description of new_task",
            "status": 2,
            "executor": 2,
            "labels": [1, 2, 3]
    }

    def setUp(self):
        self.client = Client()
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        self.task3 = Task.objects.get(pk=3)
        self.user_with_tasks = get_user_model().objects.get(pk=1)
        self.user_without_tasks = get_user_model().objects.get(pk=4)

    def test_tasks_list_without_auth(self):
        response = self.client.get(reverse_lazy('list_tasks'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/tasks/')
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

    def test_tasks_list(self):
        user = self.user_with_tasks
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('list_tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name='tasks/list_tasks.html'
        )

        tasks_list = response.context['filter']
        count_tasks_bf_create = len(Task.objects.all())
        self.assertTrue(len(tasks_list.queryset) == count_tasks_bf_create)

    def test_task_create_without_auth(self):
        response = self.client.get(reverse_lazy('create_task'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/tasks/create/')
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

    def test_task_create(self):
        user = self.user_with_tasks
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('create_task'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name='tasks/create_task.html'
        )

        count_tasks_bf_create = len(Task.objects.all())
        response_post = self.client.post(
            reverse_lazy('create_task'),
            self.input_task
        )
        count_tasks_after_create = len(Task.objects.all())
        self.assertTrue(
            count_tasks_after_create == count_tasks_bf_create + 1
        )

        new_task = Task.objects.get(pk=count_tasks_after_create)
        self.assertTrue(new_task)
        self.assertEqual(new_task.name, self.input_task['name'])
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, reverse_lazy('list_tasks'))
        response = self.client.get(reverse_lazy('list_tasks'))
        tasks_list = response.context['filter']
        self.assertTrue(
            len(tasks_list.queryset) == count_tasks_bf_create + 1
        )

    def test_task_update_without_auth(self):
        response_redirect = self.client.get(
            reverse_lazy('update_task', args=[self.task1.pk])
        )
        self.assertEqual(response_redirect.status_code, 302)
        self.assertRedirects(
            response_redirect,
            '/login/?next=/tasks/1/update/'
        )
        messages = list(get_messages(response_redirect.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Вы не авторизованы! Пожалуйста, выполните вход.")
        self.assertEqual(messages[0].level, message_constants.ERROR)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message='Вы не авторизованы! Пожалуйста, выполните вход.'
        )

    def test_task_update_using_exist_name(self):
        pass

    def test_task_update(self):
        user = self.user_without_tasks
        self.client.force_login(user)
        response = self.client.get(
            reverse_lazy('update_task', args=[self.task1.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name='tasks/update_task.html'
        )

        inputform = self.input_task
        response = self.client.post(
            reverse_lazy('update_task', args=[self.task1.pk]),
            inputform
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('list_tasks'))
        updated_task = Task.objects.get(pk=self.task1.pk)
        self.assertEqual(updated_task.name, inputform['name'])

    def test_task_delete_without_auth(self):
        response_redirect = self.client.get(
            reverse_lazy('delete_task', args=[self.task1.pk])
        )
        self.assertEqual(response_redirect.status_code, 302)
        self.assertRedirects(
            response_redirect,
            '/login/?next=/tasks/1/delete/'
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

    def test_nonself_task_delete(self):
        user = self.user_without_tasks
        task_another_user = self.task1
        self.client.force_login(user)
        count_tasks_before_del = len(Task.objects.all())
        self.client.get(
            reverse_lazy('delete_task', args=[task_another_user.pk])
        )
        count_tasks_after_del = len(Task.objects.all())
        self.assertTrue(count_tasks_after_del == count_tasks_before_del)
        self.assertRaisesMessage(
            expected_exception=ProtectedError,
            expected_message='Задачу может удалить только ее автор'
        )

    def test_self_task_delete(self):
        user = self.user_with_tasks
        self_task = self.task1
        self.client.force_login(user)
        response = self.client.get(
            reverse_lazy('delete_task', args=[self_task.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name='tasks/delete_task.html'
        )

        count_tasks_before_del = len(Task.objects.all())
        response = self.client.post(
            reverse_lazy('delete_task', args=[self_task.pk])
        )
        count_tasks_after_del = len(Task.objects.all())
        self.assertTrue(count_tasks_after_del == count_tasks_before_del - 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('list_tasks'))
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(pk=self_task.pk)
