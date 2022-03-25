from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User
from posts.tests import constants_tests as const


class PostsFormsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title=const.GROUP_TITLE,
            slug=const.GROUP_SLUG,
            description=const.GROUP_TITLE
        )

        cls.post = Post.objects.create(
            text=const.POST_TEXT,
            author=cls.user,
            group=PostsFormsTests.group
        )

    def test_create_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': const.POST_TEXT,
            'group': PostsFormsTests.group.pk,
        }
        response = self.authorized_client.post(
            const.POST_CREATE_URL_VALUES,
            data=form_data
        )
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': f'{self.user}'})
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.latest('pub_date'))
        self.assertEqual(Post.objects.latest('pub_date').text, const.POST_TEXT)

    def test_edit_post(self):
        post_id = self.post.pk
        posts_count = Post.objects.count()
        form_data = {
            'group': PostsFormsTests.group.pk,
            'text': const.POST_TEXT2,
        }
        self.authorized_client.post(
            reverse('posts:post_edit', args=(f'{post_id}',)),
            data=form_data,
            follow=False
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(Post.objects.latest('pub_date'))
        self.assertEqual(
            Post.objects.latest('pub_date').text, const.POST_TEXT2
        )
