from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User, Follow
from posts.tests import constants_tests as const


class FollowViewsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = User.objects.create_user(username='User1')
        cls.user2 = User.objects.create_user(username='User2')
        cls.user3 = User.objects.create_user(username='User3')
        cls.authorized_client = Client()
        cls.another_authorized = Client()
        cls.authorized_client.force_login(cls.user)
        cls.another_authorized.force_login(cls.user3)

        cls.group = Group.objects.create(
            title=const.GROUP_TITLE,
            slug=const.GROUP_SLUG,
            description=const.GROUP_DESCRIPTION,
        )
        for i in range(25):
            Post.objects.create(
                text=const.POST_TEXT,
                group=cls.group,
                author=cls.user
            )
        cls.post = Post.objects.create(
            text=const.POST_TEXT2,
            group=cls.group,
            author=cls.user2
        )

    def test_creates_deletes_show_follow(self):
        self.authorized_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': self.user.username}
            ),
            follow=True
        )
        new_follow = Follow.objects.filter(user=self.user)
        self.assertTrue(new_follow.count() == 0)

        self.authorized_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': self.user2.username}
            ),
            follow=True
        )
        self.another_authorized.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': self.user.username}
            ),
            follow=True
        )
        response = self.authorized_client.get(
            reverse(
                'posts:follow_index'
            ),
            follow=True
        )
        response_2 = self.another_authorized.get(
            reverse(
                'posts:follow_index'
            ),
            follow=True
        )
        new_follow = Follow.objects.filter(user=self.user)
        another_follow = Follow.objects.get(user=self.user3)
        first_object = response.context['page_obj'][0]
        another_first_object = response_2.context['page_obj'][0]
        self.assertTemplateUsed(
            response,
            'posts/follow.html'
        )
        self.assertTemplateUsed(
            response_2,
            'posts/follow.html'
        )
        self.assertTrue(new_follow.count() == 1)
        self.assertTrue(new_follow[0].author.username == 'User2')
        self.assertTrue(another_follow.author.username == 'User1')
        self.assertFalse(first_object.text == const.POST_TEXT)
        self.assertEqual(first_object.text, const.POST_TEXT2)
        self.assertTrue(another_first_object.text == const.POST_TEXT)
        self.another_authorized.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': self.user.username}
            )
        )
        deleted_follow_count = Follow.objects.filter(user=self.user3).count()
        self.assertTrue(deleted_follow_count == 0)
