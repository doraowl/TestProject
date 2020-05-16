from django.db import models

class Person(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    def json(self):
        return {
            'id':self.pk,
            'login':self.login,
            'password':self.password,
            'posts':[post.json() for post in Post.objects.filter(author_id=self.pk)]
            }

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    author=models.ForeignKey(Person, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    def json(self):
        return {
            'id':self.pk,
            'text':self.text,
            'author_id':self.author_id
            }