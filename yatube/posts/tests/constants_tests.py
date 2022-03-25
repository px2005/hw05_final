from django.urls import reverse

INDEX_URL = 'posts/index.html'
INDEX_URL_VALUES = reverse('posts:index')
GROUP_URL = 'posts/group_list.html'
GROUP_URL_VALUES = reverse('posts:group_list', kwargs={'slug': 'test-slug'})
PROFILE_URL = 'posts/profile.html'
POST_DETAIL_URL = 'posts/post_detail.html'
POST_CREATE_URL = 'posts/create_post.html'
POST_CREATE_URL_VALUES = reverse('posts:post_create')
GROUP_SLUG = 'test-slug'
GROUP_TITLE = 'Тестовая группа'
GROUP_DESCRIPTION = 'Тестовое описание'
POST_TEXT = 'Тестовый текст'
POST_TEXT2 = 'Тестовый текст2'
image = 'posts/test.jpg'
COMMENT_TEXT = 'Тестовый комментарий'
