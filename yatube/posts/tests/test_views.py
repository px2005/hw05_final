from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User
from posts.tests import constants_tests as const


class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group_object = Group.objects.create(
            title=const.GROUP_TITLE,
            slug=const.GROUP_SLUG,
            description=const.GROUP_DESCRIPTION
        )

    def setUp(self):
        self.user = User.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post = Post.objects.create(
            text=const.POST_TEXT,
            author=self.user,
            group=TaskPagesTests.group_object
        )

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            const.INDEX_URL: const.INDEX_URL_VALUES,
            const.GROUP_URL: const.GROUP_URL_VALUES,
            const.PROFILE_URL: (
                reverse('posts:profile',
                        kwargs={'username': self.user.username})
            ),
            const.POST_DETAIL_URL: (
                reverse('posts:post_detail', kwargs={'post_id': self.post.pk})
            ),
            const.POST_CREATE_URL: (
                reverse('posts:post_edit', kwargs={'post_id': self.post.pk})
            ),
        }
        templates_pages_nonames = {
            const.POST_CREATE_URL: const.POST_CREATE_URL_VALUES,
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

        for template, reverse_name in templates_pages_nonames.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(const.INDEX_URL_VALUES)
        first_object = response.context['posts'][0]
        task_text_0 = first_object.text
        self.assertEqual(task_text_0, const.POST_TEXT)

    def test_group_list_page_show_correct_context(self):
        response = self.authorized_client.get(const.GROUP_URL_VALUES)
        self.assertEqual(
            response.context.get('posts')[0].text, const.POST_TEXT
        )
        self.assertEqual(
            response.context.get('posts')[0].group.title, const.GROUP_TITLE
        )

    def test_profile_list_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        self.assertEqual(
            response.context.get('page_obj')[0].text, const.POST_TEXT
        )
        self.assertEqual(
            response.context.get('page_obj')[0].author.username, 'StasBasov'
        )

    def test_post_detail_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk})
        )
        self.assertEqual(
            response.context.get('posts').text, const.POST_TEXT
        )
        self.assertEqual(
            response.context.get('posts').pk, self.post.pk
        )

    def test_post_edit_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk})
        )
        form_fields = {
            'text': forms.fields.CharField,

        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        self.assertEqual(
            response.context.get('posts').text, const.POST_TEXT
        )
        self.assertEqual(
            response.context.get('posts').pk, self.post.pk
        )

    def test_create_post_page_show_correct_context(self):
        response = self.authorized_client.get(const.POST_CREATE_URL_VALUES)
        form_fields = {
            'text': forms.fields.CharField,

        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test3_dop_index_post_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['posts'][0]
        task_text_0 = first_object.text
        task_group_0 = first_object.group.title
        self.assertEqual(task_text_0, const.POST_TEXT)
        self.assertEqual(task_group_0, const.GROUP_TITLE)

    def test3_dop_group_post_page_show_correct_context(self):
        response = self.authorized_client.get(const.GROUP_URL_VALUES)
        self.assertEqual(
            response.context.get('posts')[0].text, const.POST_TEXT
        )
        self.assertEqual(
            response.context.get('posts')[0].group.title, const.GROUP_TITLE
        )

    def test3_dop_profile_post_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        self.assertEqual(
            response.context.get('page_obj')[0].text, const.POST_TEXT
        )
        self.assertEqual(
            response.context.get('page_obj')[0].author.username, 'StasBasov'
        )
        self.assertEqual(
            response.context.get('page_obj')[0].group.title, const.GROUP_TITLE
        )


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group_object = Group.objects.create(
            title=const.GROUP_TITLE,
            slug=const.GROUP_SLUG,
            description=const.GROUP_DESCRIPTION
        )

    def setUp(self):
        self.user = User.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        for i in range(1, 14):
            self.post = Post.objects.create(
                text=f'{const.POST_TEXT}{i}',
                author=self.user,
                group=PaginatorViewsTest.group_object
            )

    def test_index_first_page_contains_ten_records(self):
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_index_second_page_contains_three_records(self):
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_group_list_first_page_contains_ten_records(self):
        response = self.client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug'})
        )
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_group_list_second_page_contains_three_records(self):
        response = self.client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug'})
            + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_profile_first_page_contains_ten_records(self):
        response = self.client.get(
            reverse('posts:profile',
                    kwargs={'username': self.user.username})
        )
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_profile_second_page_contains_three_records(self):
        response = self.client.get(
            reverse('posts:profile',
                    kwargs={'username': self.user.username})
            + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 3)
