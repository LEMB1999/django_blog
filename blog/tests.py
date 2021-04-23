from django.contrib.auth import get_user_model
from django.test import Client,TestCase
from django.urls import reverse
from .models import Post

# Create your tests here.
class BlogTest(TestCase):
    def setUp(self):
        self.user =  get_user_model().objects.create_user(
            username="testUser",
            email='test@email.com',
            password='secret'
        )

        self.post = Post.objects.create(
            titulo = 'Un buen  título',
            cuerpo = 'Buen contenido del Cuerpo',
            autor = self.user
        )

    def test_string_representation(self):
        post = Post(titulo="Título de prueba")
        self.assertEqual(str(post),post.titulo)

    def text_post_content(self):
        self.assertEqual(f'{self.post.titulo}','Un buen  título')        
        self.assertEqual(f'{self.post.autor}', 'testUser')
        self.assertEqual(f'{self.post.cuerpo}','Buen contenido del Cuerpo')
    
    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertEqual(response,'Buen contenido del Cuerpo')
        self.assertTemplateUsed(response,'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1')
        no_response = self.client.get('/post/100000')
        self.assertEqual(response.status_code,200)
        self.assertEqual(no_response.status_code,404)
        self.assertContains(response, 'Un buen  título')
        self.assertTemplateUsed(response,'post_detail.html')


