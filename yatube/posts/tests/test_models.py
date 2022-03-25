from django.test import TestCase

from posts.models import Post, Group, User
from posts.tests import constants_tests as const


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title=const.GROUP_TITLE,
            slug=const.GROUP_SLUG,
            description=const.GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=const.POST_TEXT,
        )

    def test_models_have_correct_object_names(self):
        post = PostModelTest.post
        expected_oject_name = post.text
        self.assertEqual(expected_oject_name, str(post))
        group = PostModelTest.group
        expected_oject_name = group.title
        self.assertEqual(expected_oject_name, str(group))
