from django.test import Client, TestCase

from posts.models import Post, Group, User, Follow
from posts.tests import constants_tests as const


class FollowViewsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='User1')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title=const.GROUP_TITLE,
            slug=const.GROUP_SLUG,
            description=const.GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            text=const.POST_TEXT,
            group=cls.group,
            author=cls.user
        )

    def test_delete_show_index_hash(self):
        self.assertEqual(Post.objects.latest('pub_date').text, const.POST_TEXT)
        post1 = Post.objects.latest('pub_date')
        post1.delete()
        self.assertEqual(post1.text, const.POST_TEXT)
