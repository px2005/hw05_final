from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User, Comment
from posts.tests import constants_tests as const


class CommentPagesTests(TestCase):
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
            group=CommentPagesTests.group_object,
            image=const.image
        )
        self.comment = Comment.objects.create(
            post=self.post,
            text=const.COMMENT_TEXT,
            author=self.user,
        )

    def test_create_comment(self):
        form_data = {
            'post': self.post,
            'text': const.COMMENT_TEXT,
            'author': self.user,
        }
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.pk}),
            data=form_data
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk})
        )
        self.assertTrue(Comment.objects.latest('created'))
        self.assertEqual(Comment.objects.latest('created').text,
                         const.COMMENT_TEXT
                         )
