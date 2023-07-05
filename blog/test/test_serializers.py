from django.test import TestCase
from blog.serializers import PostSerializer, ReactionSerializer
from django.contrib.auth.models import User

from blog.models import Post, Reaction
from blog.serializers import PostSerializer, ReactionSerializer

class TestPostSerializers(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username = 'admin',
            password = '123'
        )
        self.owner = User.objects.create(
            username = 'Doniyorbek',
            password = '12321'
        )
        self.post = Post.objects.create(
            title = 'new post',
            content = 'documentation',
            author = self.user
        )
        self.post1 = Post.objects.create(
            title = 'post2',
            content = 'new doc',
            author = self.owner
        )
    
    def test_serializers_get_id(self):
        serializer = PostSerializer(instance=self.post)
        
        self.assertEqual(serializer.data["title"], 'new post')
        self.assertEqual(serializer.data['content'], 'documentation')
        self.assertEqual(serializer.data['author'], self.user.pk)
    
    def test_all_post(self):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many = True)
        
        self.assertEqual(serializer.data[0]['title'], 'new post')
        self.assertEqual(serializer.data[0]['content'], 'documentation')
        self.assertEqual(serializer.data[0]['author'], self.user.pk)
        self.assertEqual(serializer.data[1]['title'], 'post2')
        self.assertEqual(serializer.data[1]['content'], 'new doc')
        self.assertEqual(serializer.data[1]['author'], self.owner.pk)
    
    def test_creat_post(self):
        serializer = PostSerializer(
            data={
                "title": "post3",
                "content": "homework",
                "author": self.owner.pk
            }
        )
        if serializer.is_valid():
            post:Post = serializer.save()
        
        self.assertEqual(serializer.is_valid(), True, "none not validate")
        self.assertEqual(post.title, "post3")
        self.assertEqual(post.content, "homework")
        self.assertEqual(post.author, self.owner)
    
    def test_post_update(self):
        serializer = PostSerializer(
            instance=self.post1,
            data={
                'title': 'homework2',
                'content': 'update_post'
            },
            partial = True
        )
        if serializer.is_valid():
            serializer.save()
        
        self.assertEqual(serializer.is_valid(), True, "Not is valid data")
        self.assertEqual(self.post1.title, 'homework2')
        self.assertEqual(self.post1.content, 'update_post')

# test raction serializers
class TestReactionSerializers(TestCase):
    def setUp(self):
        user = User.objects.create(
            username = 'admin',
            password = 'XXX'
        )
        post = Post.objects.create(
            title = 'new post',
            content = 'documentation',
            author = user
            )
        self.reaction = Reaction.objects.create(
            user = user,
            post = post,
            like = True
            )
    def test_serializers_get_id(self):
        serializer = ReactionSerializer(instance=self.reaction)
            
        self.assertEqual(serializer.data["user"], 1)
        self.assertEqual(serializer.data["post"], 1)
        self.assertEqual(serializer.data["like"], True)
    
    def test_all_reaction(self):
        reactions = Reaction.objects.all()
        serializer = ReactionSerializer(reactions, many = True)
        
        self.assertEqual(serializer.data[0]['user'], 1)
        self.assertEqual(serializer.data[0]['post'], 1)
        self.assertEqual(serializer.data[0]['like'], True)
        
    def test_creat_reaction(self):
        serializer = ReactionSerializer(
            data={
                "user": 1,
                "post": 1,
                "like": False
            }
        )
        if serializer.is_valid():
            reaction:Reaction = serializer.save()
        
        self.assertEqual(serializer.is_valid(), True, "none not validate")
        self.assertEqual(reaction.user.pk, 1)
        self.assertEqual(reaction.post.pk, 1)
        self.assertEqual(reaction.like, False)
        
    def test_reaction_update(self):
        serializer = ReactionSerializer(
            instance=self.reaction,
            data={
                'like': False
            },
            partial = True
        )
        if serializer.is_valid():
            serializer.save()
        
        self.assertEqual(serializer.is_valid(), True, "Not is valid data")
        self.assertEqual(self.reaction.like, False)