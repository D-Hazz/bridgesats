from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import ListView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count
from .forms import SubscribersForm, BlogForm
from .models import Academie, Bitcoin, Category, Contact, Equipe, Immobilier, Informatique, Laboratoire, Partenaire, Production_Audio_Visuelle, Subscribers, CreateBlog, Comment
from django.db.models import Q
import re
from core import models # type: ignore

#Validation_email
def validate_email(email):
    # Expression régulière basique pour valider un email
    regex = r'\S+@\S+'
    if re.match(regex, email):
        return True
    else:
        return False

# home function
def accueille(request):
    list_articles = CreateBlog.objects.all()[:4]
    equipe = Equipe.objects.all()[:4]
    partenaire = Partenaire.objects.all()   
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')

        # Validation personnalisée
        errors = {}
        if not nom:
            errors['nom'] = "Le champ 'Nom' est requis"
        if not email:
            errors['email'] = "Le champ 'Email' est requis"
        # ... ajouter d'autres validations si nécessaire

        if errors:  
            return render(request, 'index.html', {'errors': errors})

        try:
            # Enregistrer les données
            contact = Contact.objects.create(
                nom=nom,
                email=email,
                sujet=sujet,
                message=message 
            )
            contact.save()
            # Message de succès et redirection
            messages.success(request, 'Merci pour la confiance accordé à BRIDGESATS ! Nous avons reçu votre message et nous vous répondons dans un bref délai')
            return redirect('accueille')
        except ValidationError as e:
            # Gestion des erreurs de validation du modèle
            errors = dict(e)
            return render(request, 'index.html', {'errors': errors})

    if request.method == 'POST':
    # Récupérer l'email directement depuis les données POST
        email = request.POST.get('email')

        # Valider l'email (vous pouvez utiliser une expression régulière ou une bibliothèque dédiée)
        if not validate_email(email):
            # Gérer l'erreur si l'email n'est pas valide
            messages.error(request, "Veuillez entrer une adresse email valide.")
            return redirect('/')

        # Créer une nouvelle instance de votre modèle et l'enregistrer
        subscriber = Subscribers(email=email)
        subscriber.save()

        # Message de succès et redirection
        messages.success(request, 'Félicitation, Vous avez rejoint notre Newsletter')
        return redirect('/')

    else:
        return render(request, 'index.html', {"liste_articles": list_articles, "equipe":equipe, "partenaire":partenaire})
    

# Blog part
def detailView(request, slug):
    # Get the post object by slug (corrected model usage)
    post = get_object_or_404(CreateBlog, slug=slug)

    # Get category and related articles
    category = post.category
    articles_en_relation = CreateBlog.objects.filter(category=category).exclude(pk=post.pk)  # Exclude current post

    # Get all categories
    list_categorys = Category.objects.all()

    # Get comments for the post
    comments = post.comments.all()
    post_comments_count = comments.count()  # Use count() method for efficiency

    # Handle POST requests for both forms (combined logic)
    if request.method == 'POST':
        if 'body' in request.POST:  # Check for comment form submission
            name = request.POST.get('name')
            body = request.POST.get('body')

            # Basic validation (improved error handling)
            if not body:
                return render(request, 'post_detail.html', {'post': post, 'error': 'Veuillez remplir tous les champs.'})

            # Create and save comment (corrected model usage)
            comment = Comment(name=name, body=body, post=post)
            comment.save()
            messages.success(request, 'Merci votre intervention')
            # Redirect after successful comment creation
            return redirect('detailView', slug=post.slug)
        else:  # Check for newsletter form submission
            form1 = SubscribersForm(request.POST)
            if form1.is_valid():
                form1.save()
                messages.success(request, 'Félicitation, Vous avez rejoint notre Newsletter')
                return redirect('detailView', slug=post.slug)

    # Handle GET requests
    else:
        form1 = SubscribersForm()  # Initialize empty form for newsletter

    # Context dictionary (concise and improved variable names)
    context = {
        'post': post,
        'comments': comments,
        'comment_count': post_comments_count,  # Renamed for clarity
        'comment_form': Comment(),  # Create empty comment object for form
        'newsletter_form': form1,
        'aer': articles_en_relation,
        'cats': list_categorys,
    }

    return render(request, 'blog-details.html', context)
def ReadCat(request, id):
    try:
        # Récupérer la catégorie et ses blogs associés
        cats = Category.objects.get(cat_id=id)
        blogs = CreateBlog.objects.filter(category=cats)

        # Récupérer le nom de la catégorie
        category_name = cats.name  # Assurez-vous que c'est le bon champ

        if request.method == 'POST':
        # Récupérer l'email directement depuis les données POST
            email = request.POST.get('email')

            # Valider l'email (vous pouvez utiliser une expression régulière ou une bibliothèque dédiée)
            if not validate_email(email):
                # Gérer l'erreur si l'email n'est pas valide
                messages.error(request, "Veuillez entrer une adresse email valide.")
                return redirect('/')

            # Créer une nouvelle instance de votre modèle et l'enregistrer
            subscriber = Subscribers(email=email)
            subscriber.save()

            # Message de succès et redirection
            messages.success(request, 'Félicitation, Vous avez rejoint la Newsletter de BRIDGESATS')
            return redirect('/')

        list_categorys = Category.objects.all()
        context = {
            'cat': cats,
            'blogs': blogs,
            'all_cats': list_categorys,
            'category_name': category_name
        }
        return render(request, 'categorie.html', context)
    except Category.DoesNotExist:
        # Gérer l'erreur si la catégorie n'existe pas
        messages.error(request, "Catégorie introuvable.")
        return redirect('/')
class BlogListView(ListView):
    model = CreateBlog
    template_name = 'blog.html'
    paginate_by = 4

    def get_queryset(self):
        queryset = CreateBlog.objects.annotate(comment_count=Count('comments'))
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(intro__icontains=query))
        queryset = CreateBlog.objects.annotate(comment_count=Count('comments'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all() 
        context['query'] = self.request.GET.get('query')
        return context
class SearchView(ListView):
    model = CreateBlog
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all() 

        return context    
def ContactForm(request):
    return redirect('accueille')


# SERVICES
def bitcoin(request):
    bitcoin = Bitcoin.objects.all()

    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email1')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')

        # Validation personnalisée
        errors = {}
        if not nom:
            errors['nom'] = "Le champ 'Nom' est requis"
        if not email:
            errors['email'] = "Le champ 'Email' est requis"
        # ... ajouter d'autres validations si nécessaire

        if errors:  
            return render(request, 'bitcoin.html', {'errors': errors, 'bitcoin': bitcoin})

        try:
            # Enregistrer les données
            contact = Contact.objects.create(
                nom=nom,
                email=email,
                sujet=sujet,
                message=message 
            )
            contact.save()
            # Message de succès et redirection
            messages.success(request, 'Merci pour la confiance accordé à BRIDGESATS ! Nous avons reçu votre message et nous vous répondons dans un bref délai')
            return redirect('bitcoin')
        except ValidationError as e:
            # Gestion des erreurs de validation du modèle
            errors = dict(e)
            return render(request, 'bitcoin.html', {'errors': errors})
    elif request.method == 'POST':
        return redirect('bitcoin')

    elif request.method == 'POST':
    # Récupérer l'email directement depuis les données POST
        email = request.POST.get('email')

        # Valider l'email (vous pouvez utiliser une expression régulière ou une bibliothèque dédiée)
        if not validate_email(email):
            # Gérer l'erreur si l'email n'est pas valide
            messages.error(request, "Veuillez entrer une adresse email valide.")
            return redirect('bitcoin')

        # Créer une nouvelle instance de votre modèle et l'enregistrer
        subscriber = Subscribers(email=email)
        subscriber.save()

        # Message de succès et redirection
        messages.success(request, 'Félicitation, Vous avez rejoint notre Newsletter')
        return redirect('bitcoin')

    else:
        return render(request, 'bitcoin.html',{'bitcoin':bitcoin})

def immobilier(request):
    immobilier = Immobilier.objects.all()

    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email1')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')

        # Validation personnalisée
        errors = {}
        if not nom:
            errors['nom'] = "Le champ 'Nom' est requis"
        if not email:
            errors['email'] = "Le champ 'Email' est requis"
        # ... ajouter d'autres validations si nécessaire

        if errors:  
            return render(request, 'votre_template.html', {'errors': errors})

        try:
            # Enregistrer les données
            contact = Contact.objects.create(
                nom=nom,
                email=email,
                sujet=sujet,
                message=message 
            )
            contact.save()
            # Message de succès et redirection
            messages.success(request, 'Merci pour la confiance accordé à BRIDGESATS ! Nous avons reçu votre message et nous vous répondons dans un bref délai')
            return redirect('immobilier')
        except ValidationError as e:
            # Gestion des erreurs de validation du modèle
            errors = dict(e)
            return render(request, 'index.html', {'errors': errors})

    if request.method == 'POST':
    # Récupérer l'email directement depuis les données POST
        email = request.POST.get('email')

        # Valider l'email (vous pouvez utiliser une expression régulière ou une bibliothèque dédiée)
        if not validate_email(email):
            # Gérer l'erreur si l'email n'est pas valide
            messages.error(request, "Veuillez entrer une adresse email valide.")
            return redirect('immobilier')

        # Créer une nouvelle instance de votre modèle et l'enregistrer
        subscriber = Subscribers(email=email)
        subscriber.save()

        # Message de succès et redirection
        messages.success(request, 'Félicitation, Vous avez rejoint notre Newsletter')
        return redirect('immobilier')

    else:
        return render(request, 'immobilier.html',{'immobilier':immobilier})
def informatique(request):
    informatique = Informatique.objects.all()

    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')

        # Validation personnalisée
        errors = {}
        if not nom:
            errors['nom'] = "Le champ 'Nom' est requis"
        if not email:
            errors['email'] = "Le champ 'Email' est requis"
        # ... ajouter d'autres validations si nécessaire

        if errors:  
            return render(request, 'votre_template.html', {'errors': errors})

        try:
            # Enregistrer les données
            contact = Contact.objects.create(
                nom=nom,
                email=email,
                sujet=sujet,
                message=message 
            )
            contact.save()
            # Message de succès et redirection
            messages.success(request, 'Merci pour la confiance accordé à BRIDGESATS ! Nous avons reçu votre message et nous vous répondons dans un bref délai')
            return redirect('informatique')
        except ValidationError as e:
            # Gestion des erreurs de validation du modèle
            errors = dict(e)
            return render(request, 'index.html', {'errors': errors})

    if request.method == 'POST':
    # Récupérer l'email directement depuis les données POST
        email = request.POST.get('email')

        # Valider l'email (vous pouvez utiliser une expression régulière ou une bibliothèque dédiée)
        if not validate_email(email):
            # Gérer l'erreur si l'email n'est pas valide
            messages.error(request, "Veuillez entrer une adresse email valide.")
            return redirect('informatique')

        # Créer une nouvelle instance de votre modèle et l'enregistrer
        subscriber = Subscribers(email=email)
        subscriber.save()

        # Message de succès et redirection
        messages.success(request, 'Félicitation, Vous avez rejoint notre Newsletter')
        return redirect('informatique')

    else:
        return render(request, 'informatique.html',{'informatique':informatique})
def academie(request):
    academie = Academie.objects.all()

    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')

        # Validation personnalisée
        errors = {}
        if not nom:
            errors['nom'] = "Le champ 'Nom' est requis"
        if not email:
            errors['email'] = "Le champ 'Email' est requis"
        # ... ajouter d'autres validations si nécessaire

        if errors:  
            return render(request, 'votre_template.html', {'errors': errors})

        try:
            # Enregistrer les données
            contact = Contact.objects.create(
                nom=nom,
                email=email,
                sujet=sujet,
                message=message 
            )
            contact.save()
            # Message de succès et redirection
            messages.success(request, 'Merci pour la confiance accordé à BRIDGESATS ! Nous avons reçu votre message et nous vous répondons dans un bref délai')
            return redirect('academie')
        except ValidationError as e:
            # Gestion des erreurs de validation du modèle
            errors = dict(e)
            return render(request, 'index.html', {'errors': errors})

    if request.method == 'POST':
    # Récupérer l'email directement depuis les données POST
        email = request.POST.get('email')

        # Valider l'email (vous pouvez utiliser une expression régulière ou une bibliothèque dédiée)
        if not validate_email(email):
            # Gérer l'erreur si l'email n'est pas valide
            messages.error(request, "Veuillez entrer une adresse email valide.")
            return redirect('academie')

        # Créer une nouvelle instance de votre modèle et l'enregistrer
        subscriber = Subscribers(email=email)
        subscriber.save()

        # Message de succès et redirection
        messages.success(request, 'Félicitation, Vous avez rejoint notre Newsletter')
        return redirect('academie')

    else:
        return render(request, 'academie.html',{'academie':academie})
def production(request):
    production = Production_Audio_Visuelle.objects.all()

    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')

        # Validation personnalisée
        errors = {}
        if not nom:
            errors['nom'] = "Le champ 'Nom' est requis"
        if not email:
            errors['email'] = "Le champ 'Email' est requis"
        # ... ajouter d'autres validations si nécessaire

        if errors:  
            return render(request, 'votre_template.html', {'errors': errors})

        try:
            # Enregistrer les données
            contact = Contact.objects.create(
                nom=nom,
                email=email,
                sujet=sujet,
                message=message 
            )
            contact.save()
            # Message de succès et redirection
            messages.success(request, 'Merci pour la confiance accordé à BRIDGESATS ! Nous avons reçu votre message et nous vous répondons dans un bref délai')
            return redirect('production')
        except ValidationError as e:
            # Gestion des erreurs de validation du modèle
            errors = dict(e)
            return render(request, 'index.html', {'errors': errors})

    if request.method == 'POST':
    # Récupérer l'email directement depuis les données POST
        email = request.POST.get('email')

        # Valider l'email (vous pouvez utiliser une expression régulière ou une bibliothèque dédiée)
        if not validate_email(email):
            # Gérer l'erreur si l'email n'est pas valide
            messages.error(request, "Veuillez entrer une adresse email valide.")
            return redirect('production')

        # Créer une nouvelle instance de votre modèle et l'enregistrer
        subscriber = Subscribers(email=email)
        subscriber.save()

        # Message de succès et redirection
        messages.success(request, 'Félicitation, Vous avez rejoint notre Newsletter')
        return redirect('production')

    else:
        return render(request, 'production.html',{'production':production})
def laboratoire(request):
    laboratoire = Laboratoire.objects.all()

    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')

        # Validation personnalisée
        errors = {}
        if not nom:
            errors['nom'] = "Le champ 'Nom' est requis"
        if not email:
            errors['email'] = "Le champ 'Email' est requis"
        # ... ajouter d'autres validations si nécessaire

        if errors:  
            return render(request, 'votre_template.html', {'errors': errors})

        try:
            # Enregistrer les données
            contact = Contact.objects.create(
                nom=nom,
                email=email,
                sujet=sujet,
                message=message 
            )
            contact.save()
            # Message de succès et redirection
            messages.success(request, 'Merci pour la confiance accordé à BRIDGESATS ! Nous avons reçu votre message et nous vous répondons dans un bref délai')
            return redirect('laboratoire')
        except ValidationError as e:
            # Gestion des erreurs de validation du modèle
            errors = dict(e)
            return render(request, 'index.html', {'errors': errors})

    if request.method == 'POST':
    # Récupérer l'email directement depuis les données POST
        email = request.POST.get('email')

        # Valider l'email (vous pouvez utiliser une expression régulière ou une bibliothèque dédiée)
        if not validate_email(email):
            # Gérer l'erreur si l'email n'est pas valide
            messages.error(request, "Veuillez entrer une adresse email valide.")
            return redirect('laboratoire')

        # Créer une nouvelle instance de votre modèle et l'enregistrer
        subscriber = Subscribers(email=email)
        subscriber.save()

        # Message de succès et redirection
        messages.success(request, 'Félicitation, Vous avez rejoint notre Newsletter')
        return redirect('laboratoire')

    else:
        return render(request, 'laboratoire.html',{'laboratoire':laboratoire})


# Correspondance
def equipe(request):
    equipe = Equipe.objects.all()
    return render(request, 'team.html', {"equipe": equipe})
def contact(request):
    contact = Contact.objects.all()
    return render(request, 'message.html', {"contact": contact})


# Services Catalogue Download
def download_academie_file(request, file_id):
    academie = get_object_or_404(Academie, id=file_id)
    if academie.catalogue:
        file = open(academie.catalogue.path, 'rb')
        response = HttpResponse(file, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="%s"' % academie.catalogue.name
        return response
    else:
        # Handle case where file doesn't exist
        return HttpResponse("Document non trouvé")        
def download_bitcoin_file(request, file_id):
    bitcoin = get_object_or_404(Bitcoin, id=file_id)
    if bitcoin.catalogue:
        file = open(bitcoin.catalogue.path, 'rb')
        response = HttpResponse(file, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="%s"' % bitcoin.catalogue.name
        return response
    else:
        # Handle case where file doesn't exist
        return HttpResponse("Document non trouvé")      
def download_info_file(request, file_id):
    info = get_object_or_404(Informatique, id=file_id)
    if info.catalogue:
        file = open(info.catalogue.path, 'rb')
        response = HttpResponse(file, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="%s"' % info.catalogue.name
        return response
    else:
        # Handle case where file doesn't exist
        return HttpResponse("Document non trouvé")       
def download_immobilier_file(request, file_id):
    immobilier = get_object_or_404(Immobilier, id=file_id)
    if immobilier.catalogue:
        file = open(immobilier.catalogue.path, 'rb')
        response = HttpResponse(file, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="%s"' % immobilier.catalogue.name
        return response
    else:
        # Handle case where file doesn't exist
        return HttpResponse("Document non trouvé")       
def download_labo_file(request, file_id):
    labo = get_object_or_404(Laboratoire, id=file_id)
    if labo.catalogue:
        file = open(labo.catalogue.path, 'rb')
        response = HttpResponse(file, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="%s"' % labo.catalogue.name
        return response
    else:
        # Handle case where file doesn't exist
        return HttpResponse("Document non trouvé")
def download_production_file(request, file_id):
    production = get_object_or_404(Production_Audio_Visuelle, id=file_id)
    if production.catalogue:
        file = open(production.catalogue.path, 'rb')
        response = HttpResponse(file, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="%s"' % production.catalogue.name
        return response
    else:
        # Handle case where file doesn't exist
        return HttpResponse("Document non trouvé") 