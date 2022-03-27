from http import HTTPStatus

from django.test import TestCase, Client

from posts.models import Group, Post, User
from posts.tests import constants_tests as const


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Group.objects.create(
            title=const.GROUP_TITLE,
            slug=const.GROUP_SLUG,
            description=const.GROUP_DESCRIPTION
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.user2 = User.objects.create_user(username='test_edit')
        self.authorized_client2 = Client()
        self.authorized_client2.force_login(self.user2)
        self.post = Post.objects.create(
            text=const.POST_TEXT,
            author=self.user
        )

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            const.INDEX_URL: '/',
            const.GROUP_URL: f'/group/{const.GROUP_SLUG}/',
            const.PROFILE_URL: f'/profile/{self.user.username}/',
            const.POST_DETAIL_URL: f'/posts/{self.post.pk}/',
            const.POST_CREATE_URL: f'/posts/{self.post.pk}/edit/',
        }
        templates_url_nonames = {
            'posts/create_post.html': '/create/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

        for template, address in templates_url_nonames.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

        response = self.authorized_client2.get(f'/posts/{self.post.pk}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_urls_nouser_uses_correct_template(self):
        templates_nouser_url_names = {
            const.INDEX_URL: '/',
            const.GROUP_URL: f'/group/{const.GROUP_SLUG}/',
            const.PROFILE_URL: f'/profile/{self.user.username}/',
            const.POST_DETAIL_URL: f'/posts/{self.post.pk}/',
        }
        for template, address in templates_nouser_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_task_list_url_redirect_anonymous(self):
        response = self.guest_client.get(f'/posts/{self.post.pk}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.guest_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_unexisting_page_404(self):
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
