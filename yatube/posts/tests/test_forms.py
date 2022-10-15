from django.test import Client, TestCase
from posts.models import User, Group, Post
from posts.forms import PostForm
from django.urls import reverse


class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовое описание',
            slug='test-slug',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
        )
        cls.form = PostForm()

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'текст поста',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data
        )
        self.assertRedirects(response, reverse('posts:profile',
                             kwargs={'username': 'test_user'}))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(
            text='Тестовый текст',
            author=self.user,
            group=self.group,
        ).exists())

    def test_post_edit(self):
        form_data = {
            'text': 'текст новый',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}),
            data=form_data,
        )
        self.assertRedirects(response, reverse('posts:post_detail',
                             kwargs={'post_id': self.post.pk}))
        self.post.refresh_from_db()
        self.assertEqual(self.post.text, 'текст новый')
