from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .instagram import Instgram
from .models import *
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def home(request):
    ip = get_ip(request)
    photos = Photo.objects.all()
    albums = Album.objects.all()
    if request.user.is_authenticated:
        Log(ip = ip, action = "Visite Home Page", login = request.user).save()
    else:
        Log(ip = ip, action = "Visite Home Page", login = "Not Login").save()

    all_photos = Paginator(photos, 15)
    page = request.GET.get('page')
    try:
        photo = all_photos.page(page)        
    except PageNotAnInteger:
        photo = all_photos.page(1)
    except EmptyPage:
        photo = all_photos.pagea(all_photos.page(all_photos.num_pages))
    
    return render(request, 'index.html', {'photos': photo, 'albums': albums, 'all_p': all_photos})


def about(request):
    ip = get_ip(request)
    if request.user.is_authenticated:
        Log(ip = ip, action = "Visite About Page", login = request.user).save()
    else:
        Log(ip = ip, action = "Visite About Page", login = "Not Login").save()

    members = Staff_user.objects.all()

    return render(request, 'about.html', {'members': members})


def contact(request):
    ip = get_ip(request)

    if request.method == "POST":
        try:
            data = request.POST
            data = dict(data)
            Contact(name = data['name'][0], mail = data['mail'][0], desc = data['desc'][0]).save()
            messages.success(request, "Hey Buddy, We Get Your Message. We Will Contact Soon.")
        except:
            return redirect(Error)

    if request.user.is_authenticated:
        Log(ip = ip, action = "Visite Contact Page", login = request.user).save()
    else:
        Log(ip = ip, action = "Visite Contact Page", login = "Not Login").save()
    return render(request, 'contact.html')


def collections(request):
    albums = Album.objects.all()
    ip = get_ip(request)

    if request.user.is_authenticated:
        Log(ip = ip, action = "Visite Albums Page", login = request.user).save()
    else:
        Log(ip = ip, action = "Visite Albums Page", login = "Not Login").save()
    return render(request, 'albums.html', {'albums': albums})


def albums_details(request, slug):
    ip = get_ip(request)
    if request.user.is_authenticated:
        Log(ip = ip, action = "Visite Albums Page", login = request.user).save()
    else:
        Log(ip = ip, action = "Visite Albums Page", login = "Not Login").save()
    try:
        album = Album.objects.filter(url_slug = slug)[0]
        photos = Photo.objects.filter(album = album)
        return render(request, 'albums-details.html', {"photos": photos})
    except:
        return redirect(Error)

    # return render(request, 'albums-details.html')


def instagram(request):
    # posts = Instgram.get_media()
    posts = {'urls': ['https://scontent.cdninstagram.com/v/t51.29350-15/148415188_869717680519430_4218630319787364712_n.jpg?_nc_cat=109&ccb=1-3&_nc_sid=8ae9d6&_nc_ohc=vhAwVXCC5cAAX8NOX5l&_nc_ht=scontent.cdninstagram.com&oh=352e203cad91e75412a955059afdb352&oe=60BA89F1', 'https://scontent.cdninstagram.com/v/t51.2885-15/62192237_320985935509293_7674802452956781516_n.jpg?_nc_cat=106&ccb=1-3&_nc_sid=8ae9d6&_nc_ohc=FLAbOvOW6FoAX_LS2f8&_nc_ht=scontent.cdninstagram.com&oh=610ad0137e574d238a685d13ff1472a7&oe=60B92789', 'https://scontent.cdninstagram.com/v/t51.2885-15/53423911_2379963262248493_4554736310909051640_n.jpg?_nc_cat=105&ccb=1-3&_nc_sid=8ae9d6&_nc_ohc=REKsbMRTG-QAX9amnnY&_nc_ht=scontent.cdninstagram.com&oh=eb30206be48f4044c0c89f5f35053271&oe=60BA3A15', 'https://scontent.cdninstagram.com/v/t51.2885-15/47694547_1994470947269193_7579978220051906786_n.jpg?_nc_cat=103&ccb=1-3&_nc_sid=8ae9d6&_nc_ohc=NizjJTt7dv8AX8TLva7&_nc_ht=scontent.cdninstagram.com&oh=3fc71f433d2bd74a53ebfaf8361ea26e&oe=60B8EE76'], 'comments': [['Ek no. Beti 🔥🔥🔥', 'Kuchh jyada hi nhi khush lg rha h tu jpr jakr.. itna to m bhi nhi hui Delhi aakr....kya mil gya be aisa...😜😜😜😜', 'Killer bro 🔥🔥😍😍', 'Oh bhaii 🔥❤️', '👌👌🔥🔥🔥😎', '🔥', 'Bete moj kar di😂😂😂😂', 'B', 'Life ko enjoy kese krr rhe ho bhai 🙄🙄🙄 hme bhi bta do', '😍😍🔥❤️'], ['wahh', 'Kaisi h movie', '😑', 'bta to deta yrr', '😘😘😍😉'], ['😎😎😎', '😂😂😉', 'Wha meri jaan👌😜'], ['Hero lg rha h yrr', '😂😉']], 'caption': ["#dark #blacklove #india\n #nagar #home Life is the biggest party you'll ever be at.😉😎", 'Enjoying #kabirsingh \n#its_p.k #bollywood', 'Memories 🙄☺😯😯']} 
    urls = posts['urls']
    comments = posts['comments']
    # caption = posts['caption']
    return render(request, 'instagram.html', {'urls': urls, 'comments': comments})


# @login_required
def upload_pics(request):
    ip = get_ip(request)
    categorys = Category.objects.all()
    albums = Album.objects.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
        else:
            user = User.objects.filter(username = 'anonymous')[0]
        images = request.FILES
        data = request.POST
        data = dict(data)
        images = dict(images)
        # print(data['name'][0])
        al = Album.objects.filter(name = data['album'][0])[0]
        cat = Category.objects.filter(name = data['category'][0])[0]
        # print(data['caption'][0])
        # print(data['category'][0])
        
        for d in images['images']:
            Photo(
                name = data['name'][0],
                user = user, 
                image = d, 
                album = al, 
                category = cat, 
                caption = data['caption'][0]
            ).save()

        if request.user.is_authenticated:
            Log(ip = ip, action = "Photo Uploaded", login = request.user).save()
        else:
            Log(ip = ip, action = "Photo Uploaded", login = "Not Login").save()
        messages.success(request, "Photo Uploaded Successfully")
        # return redirect(upload_pics)
        # return render(request, 'upload-pics.html', {'categorys': categorys, 'albums': albums})
        return redirect(home)

    else:
        if request.user.is_authenticated:
            Log(ip = ip, action = "Visite Upload Page", login = request.user).save()
        else:
            Log(ip = ip, action = "Visite Upload Page", login = "Not Login").save()
        
        

        
        return render(request, 'upload-pics.html', {'categorys': categorys, 'albums': albums})


def Error(request):
    return render(request, '404.html')