from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from froala_editor.fields import FroalaField
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='media/uploads/')
User = get_user_model()


class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class CreateBlog(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    intro = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=1000, unique=True, blank=True)
    body = models.TextField()
    image = models.ImageField(upload_to='media')
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']

    def save(self, *args, **kargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kargs)

    def author_or_default(self):
        return self.author.username if self.author else "L'auteur inconnu"


class Comment(models.Model):
    post = models.ForeignKey(CreateBlog, related_name='comments', on_delete=models.CASCADE)
    email = models.EmailField()
    body = models.TextField()
    name = models.CharField(max_length=100, default="inconnue")
    # name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']

        def __str__(self):
            return self.user.username


# Create your models here.
class Subscribers(models.Model):
    email = models.EmailField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class MailMessage(models.Model):
    tilte = models.CharField(max_length=1000, null=True)
    message = FroalaField()

    def __str__(self):
        return self.tilte


class Partenaire(models.Model):
    nom = models.URLField(max_length=200, help_text="Entrez l'URL du site web")
    image = models.ImageField(upload_to='media')
    
    def __str__(self):
        return self.nom


class Equipe(models.Model):
    nom = models.CharField(max_length=120)
    image = models.ImageField(upload_to='media')
    fonction = models.CharField(max_length=1000, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    linkedin = models.CharField(max_length=1000, blank=True, null=True)
    github = models.CharField(max_length=1000, blank=True, null=True)
    tweeter = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.nom

class Contact(models.Model):
    nom = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    sujet = models.CharField(max_length=1000, null=True, blank=True)
    message = models.TextField()
    date_added = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.email

class Bitcoin(models.Model):
    catalogue = models.FileField(verbose_name='Bitcoin_catalogue', upload_to='media/bitcoin', blank="True", null="True")
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    intro = models.TextField()
    redacteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=1000, unique=True, blank=True)
    description1 = FroalaField(null=True, blank=True)
    description2 = FroalaField(null=True, blank=True)
    description3 = FroalaField(null=True, blank=True)
    description4 = FroalaField(null=True, blank=True)
    image_entete = models.ImageField(upload_to='media/bitcoin',null=True, blank=True)
    image1 = models.ImageField(upload_to='media/bitcoin', null=True, blank=True)
    image2 = models.ImageField(upload_to='media/bitcoin', null=True, blank=True)   
    image3 = models.ImageField(upload_to='media/bitcoin', null=True, blank=True)
    image4 = models.ImageField(upload_to='media/bitcoin', null=True, blank=True)
    date_added = models.DateTimeField(auto_now=True)
    kiveclair_url = models.URLField(max_length=2000, help_text="Entrez l'URL de kiveclair")

    class Meta:
        ordering = ['-date_added']

class Laboratoire(models.Model):
    catalogue = models.FileField(verbose_name='Laboratoire_catalogue', upload_to='media/labo', blank="True", null="True")
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    intro = models.TextField()
    redacteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=1000, unique=True, blank=True)
    description1 = FroalaField(null=True, blank=True)
    description2 = FroalaField(null=True, blank=True)
    description3 = FroalaField(null=True, blank=True)
    description4 = FroalaField(null=True, blank=True)
    image_entete = models.ImageField(upload_to='media/labo',null=True, blank=True)
    image1 = models.ImageField(upload_to='media/labo', null=True, blank=True)
    image2 = models.ImageField(upload_to='media/labo', null=True, blank=True)   
    image3 = models.ImageField(upload_to='media/labo', null=True, blank=True)
    image4 = models.ImageField(upload_to='media/labo', null=True, blank=True)   
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']

class Immobilier(models.Model):
    catalogue = models.FileField(verbose_name='Immobilier_catalogue', upload_to='media/immobilier', blank="True", null="True")
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    intro = models.TextField()
    redacteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=1000, unique=True, blank=True)
    description1 = FroalaField(null=True, blank=True)
    description2 = FroalaField(null=True, blank=True)
    description3 = FroalaField(null=True, blank=True)
    description4 = FroalaField(null=True, blank=True)
    image_entete = models.ImageField(upload_to='media/immobilier',null=True, blank=True)
    image1 = models.ImageField(upload_to='media/immobilier', null=True, blank=True)
    image2 = models.ImageField(upload_to='media/immobilier', null=True, blank=True)   
    image3 = models.ImageField(upload_to='media/immobilier', null=True, blank=True)
    image4 = models.ImageField(upload_to='media/immobilier', null=True, blank=True) 
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']

class Informatique(models.Model):
    catalogue = models.FileField(verbose_name='Informatique_catalogue', upload_to='media/info', blank="True", null="True")
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    intro = models.TextField()
    redacteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=1000, unique=True, blank=True)
    description1 = FroalaField(null=True, blank=True)
    description2 = FroalaField(null=True, blank=True)
    description3 = FroalaField(null=True, blank=True)
    description4 = FroalaField(null=True, blank=True)
    image_entete = models.ImageField(upload_to='media/info',null=True, blank=True)
    image1 = models.ImageField(upload_to='media/info', null=True, blank=True)
    image2 = models.ImageField(upload_to='media/info', null=True, blank=True)   
    image3 = models.ImageField(upload_to='media/info', null=True, blank=True)
    image4 = models.ImageField(upload_to='media/info', null=True, blank=True)   
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']

class Academie(models.Model):
    catalogue = models.FileField(verbose_name='Academie_catalogue', upload_to='media/academie',storage=fs, blank="True", null="True")
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    intro = models.TextField()
    redacteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=1000, unique=True, blank=True)
    description1 = FroalaField(null=True, blank=True)
    description2 = FroalaField(null=True, blank=True)
    description3 = FroalaField(null=True, blank=True)
    description4 = FroalaField(null=True, blank=True)
    image_entete = models.ImageField(upload_to='media/academie',null=True, blank=True)
    image1 = models.ImageField(upload_to='media/academie', null=True, blank=True)
    image2 = models.ImageField(upload_to='media/academie', null=True, blank=True)   
    image3 = models.ImageField(upload_to='media/academie', null=True, blank=True)
    image4 = models.ImageField(upload_to='media/academie', null=True, blank=True)   
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']


class Production_Audio_Visuelle(models.Model):
    catalogue = models.FileField(verbose_name='Production_catalogue', upload_to='media/production', blank="True", null="True")
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    intro = models.TextField()
    redacteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=1000, unique=True, blank=True)
    description1 = FroalaField(null=True, blank=True)
    description2 = FroalaField(null=True, blank=True)
    description3 = FroalaField(null=True, blank=True)
    description4 = FroalaField(null=True, blank=True)
    image_entete = models.ImageField(upload_to='media/production',null=True, blank=True)
    image1 = models.ImageField(upload_to='media/production', null=True, blank=True)
    image2 = models.ImageField(upload_to='media/production', null=True, blank=True)   
    image3 = models.ImageField(upload_to='media/production', null=True, blank=True)
    image4 = models.ImageField(upload_to='media/production', null=True, blank=True)  
    date_added = models.DateTimeField(auto_now=True)
    youtube_url = models.URLField(max_length=2000, help_text="Entrez l'URL de youtube")
    podcast_url = models.URLField(max_length=2000, help_text="Entrez l'URL des podcasts")

    class Meta:
        ordering = ['-date_added']