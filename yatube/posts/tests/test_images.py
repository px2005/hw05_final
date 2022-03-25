from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User
from posts.tests import constants_tests as const


class ImagePagesTests(TestCase):
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
            group=ImagePagesTests.group_object,
            image=const.image
        )

    def test_index_image_show_correct_context(self):
        response = self.authorized_client.get(const.INDEX_URL_VALUES)
        first_object = response.context['posts'][0]
        task_image_0 = first_object.image
        self.assertEqual(task_image_0, const.image)

    def test_profile_image_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        self.assertEqual(
            response.context.get('page_obj')[0].image, const.image
        )

    def test_group_list_image_show_correct_context(self):
        response = self.authorized_client.get(const.GROUP_URL_VALUES)
        self.assertEqual(
            response.context.get('posts')[0].image, const.image
        )

    def test_post_detail_image_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk})
        )
        self.assertEqual(
            response.context.get('posts').image, const.image
        )

    def test_create_post_image(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': const.POST_TEXT,
            'group': ImagePagesTests.group_object.pk,
            'image': const.image,
        }
        response = self.authorized_client.post(
            const.POST_CREATE_URL_VALUES,
            data=form_data
        )
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': self.user})
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.latest('pub_date'))
        self.assertEqual(Post.objects.latest('pub_date').text, const.POST_TEXT)
