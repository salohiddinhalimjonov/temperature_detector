from django.shortcuts import render, redirect, get_object_or_404  #
import serial
# The render function Combines a given template with a given context dictionary and
# returns an HttpResponse object with that rendered text.
# You request a page and the render function returns it.
# The redirect function sends another request to the given url.
from .models import AboutUrl, CustomUser
from django.views import View  # class based view
from .forms import UrlForm
from django.http import HttpResponse
from datetime import datetime
from django.core.paginator import Paginator
from .filter import ChoiceFilter
from .forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.mail import \
    EmailMultiAlternatives  # A version of EmailMessage that makes it easy to send multipart/alternative messages.
# For example, including text and HTML versions of the text is made easier.
from django.core.mail import send_mail
from django.template.loader import get_template  # or loading templates
from django.template import Context  # holds some metadata in addition to the context data.
# It is passed to Template.render() for rendering a template.
from django.db.models import Q  # We can search title and url in search with using this function
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth import update_session_auth_hash  # This is used for changing password
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail  # .BadHeaderError: Header values can't contain newlines
from django.template.loader import \
    render_to_string  # loads a template like get_template() and calls its render() method immediately.
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
import random
# MatPlotLib
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np

class RegisterUser(View):
    def get(self, request):

        form = UserRegisterForm()  # If we arrive at this view with a GET request,
        # it will create an empty form instance and place it in the template context to be rendered.
        context = {'form': form}
        template = 'registration/register.html'
        return render(request, template, context)

    def post(self, request):
        form = UserRegisterForm(request.POST, request.FILES)  # request.Files is used for handling image
        # If the form is submitted using a POST request, the view will once again create a form instance and populate it with data from the request:
        # form = NameForm(request.POST) This is called “binding data to the form” (it is now a bound form).
        if form.is_valid():

            form.save()  # this automatically saves cleaned_data of the form instance
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get(
                'email')  # form.cleaned_data returns a dictionary of validated form input fields and their values,
            # where string primary keys are returned as objects({'username': 'xyz', 'password': 'shinchan'})
            # form.data returns a dictionary of un-validated form input fields and
            # their values in string format (<tr><th><label for="id_username">Username:...).
            # form.cleaned_data['f1'] -- cleaned data request.POST.get('f1') -- un-validated data
            smth = authenticate(request, email=email, password=password)
            # Use authenticate() to verify a set of credentials. It takes credentials as keyword arguments, username and password for the default case,
            # checks them against each authentication backend, and returns a User object if the credentials are valid for a backend.
            # If the credentials aren’t valid for any backend or if a backend raises PermissionDenied, it returns None.
            if smth is not None:
                login(request,
                      smth)  # To log a user in, from a view, use login(). It takes an HttpRequest object and a User object. login() saves the user’s ID in the session,
                # using Django’s session framework.

                return redirect('home')  # it redirects to the page with the path name of 'home'
        return render(request, 'registration/register.html', {'form': form})


class Login(View):
    def get(self, request):

        username = request.POST.get('username')  # this is unvalidated data
        password = request.POST.get('password')
        context = {'username': username, 'password': password}
        return render(request, 'registration/login.html', context)

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect('home')
        else:
            messages.info(request, f'Invalid email or password!')
        context = {'username': username, 'password': password}
        return render(request, 'registration/login.html', context)


class Logout(View):
    def get(self, request):
        pass

    def post(self, request):
        logout(request)
        return redirect('login')


class ChangePassword(View):
    def get(self, request):
        form = PasswordChangeForm(request.user)  # it takes an user argument in its constructor.
        context = {'form': form}
        return render(request, 'registration/password_change.html', context)

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)  # it takes an user argument in its constructor.
        # it changes the password of authenticated user
        context = {'form': form}
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            # Updating a user's password logs out all sessions for the user
            # if django.contrib.auth.middleware.SessionAuthenticationMiddleware is enabled.

            # This function takes the current request and the updated user object from which
            # the new session hash will be derived and updates the session hash appropriately to prevent
            # a password change from logging out the session from which the password was changed.

            return redirect('password_changed')
        else:
            pass

        return render(request, 'registration/password_change.html', context)


class PasswordResetRequest(View):
    def get(self, request):
        domain = request.headers[
            'Host']  # request.headers : A case insensitive, dict-like object that provides access to all HTTP-prefixed headers
        password_reset_form = PasswordResetForm(request.GET)
        return render(request, 'registration/reset_password.html',
                      {'domain': domain, 'password_reset_form': password_reset_form})

    def post(self, request):
        domain = request.headers['Host']
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(email=data)
            if associated_users:
                for user in associated_users:
                    subject = 'Password Reset Requested'
                    email_template_name = 'registration/password_reset_email.txt'
                    c = {
                        'email': user.email,
                        'domain': domain,
                        'site_name': 'Interface',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found!')
                    return redirect('reset_done')

        password_reset_form = PasswordResetForm()
        return render(request, 'registration/reset_password.html', {'password_reset_form': password_reset_form})


class Home(View):

    def get(self, request):

        if request.user.is_authenticated:
            customer = CustomUser.objects.get(email=request.user.email)
            allurls_count = customer.abouturl_set.all().count()  # abouturl is lowercase of AboutUrl model name. It gets all urls created by the current user
            importanturls_count = customer.abouturl_set.filter(choices='Important').count()
            almostimportanturls_count = customer.abouturl_set.filter(choices='Almost Important').count()
            notimportanturls_count = customer.abouturl_set.filter(choices='Not Important').count()
            search = request.GET.get('search')
            if search is not None:
                smth = AboutUrl.objects.filter(Q(title__contains=search) | Q(original_url=search),
                                               user=request.user).order_by('-pk')

                paginator = Paginator(smth, 4)  # show 4 urls per page
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)



            else:

                smth = AboutUrl.objects.filter(user=request.user).order_by('-pk')

                paginator = Paginator(smth, 4)  #
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)

            return render(request, 'home.html',
                          {'list': smth, 'page_obj': page_obj, 'search': search, 'customer': customer,
                           'allurls_count': allurls_count, 'importanturls_count': importanturls_count,
                           'almostimportanturls_count': almostimportanturls_count,
                           'notimportanturls_count': notimportanturls_count})
        else:

            return render(request, 'home.html')


class HomeImportant(View):

    def get(self, request):

        if request.user.is_authenticated:
            customer = CustomUser.objects.get(email=request.user.email)
            allurls_count = customer.abouturl_set.all().count()
            importanturls_count = customer.abouturl_set.filter(choices='Important').count()
            almostimportanturls_count = customer.abouturl_set.filter(choices='Almost Important').count()
            notimportanturls_count = customer.abouturl_set.filter(choices='Not Important').count()
            search = request.GET.get('search', None)
            if search is not None:
                smth = AboutUrl.objects.filter(Q(title__contains=search) | Q(original_url=search),
                                               user=request.user).order_by('-pk')

                paginator = Paginator(smth, 4)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)



            else:

                smth = AboutUrl.objects.filter(choices='Important', user=request.user).order_by('-pk')

                paginator = Paginator(smth, 4)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)

            return render(request, 'home.html',
                          {'list': smth, 'page_obj': page_obj, 'search': search, 'customer': customer,
                           'allurls_count': allurls_count, 'importanturls_count': importanturls_count,
                           'almostimportanturls_count': almostimportanturls_count,
                           'notimportanturls_count': notimportanturls_count})
        else:

            return render(request, 'home.html')


class HomeAlmostImportant(View):

    def get(self, request):

        if request.user.is_authenticated:

            customer = CustomUser.objects.get(email=request.user.email)
            allurls_count = customer.abouturl_set.all().count()
            importanturls_count = customer.abouturl_set.filter(choices='Important').count()
            almostimportanturls_count = customer.abouturl_set.filter(choices='Almost Important').count()
            notimportanturls_count = customer.abouturl_set.filter(choices='Not Important').count()
            search = request.GET.get('search', None)
            if search is not None:
                smth = AboutUrl.objects.filter(Q(title__contains=search) | Q(original_url=search),
                                               user=request.user).order_by('-pk')

                paginator = Paginator(smth, 4)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)



            else:

                smth = AboutUrl.objects.filter(choices='Almost Important', user=request.user).order_by('-pk')

                paginator = Paginator(smth, 4)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)

            return render(request, 'home.html',
                          {'list': smth, 'page_obj': page_obj, 'search': search, 'customer': customer,
                           'allurls_count': allurls_count, 'importanturls_count': importanturls_count,
                           'almostimportanturls_count': almostimportanturls_count,
                           'notimportanturls_count': notimportanturls_count})
        else:

            return render(request, 'home.html')


class HomeNotImportant(View):

    def get(self, request):

        if request.user.is_authenticated:
            customer = CustomUser.objects.get(email=request.user.email)
            allurls_count = customer.abouturl_set.all().count()
            importanturls_count = customer.abouturl_set.filter(choices='Important').count()
            almostimportanturls_count = customer.abouturl_set.filter(choices='Almost Important').count()
            notimportanturls_count = customer.abouturl_set.filter(choices='Not Important').count()
            search = request.GET.get('search', None)
            if search is not None:
                smth = AboutUrl.objects.filter(Q(title__contains=search) | Q(original_url=search),
                                               user=request.user).order_by('-pk')

                paginator = Paginator(smth, 4)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)



            else:

                smth = AboutUrl.objects.filter(choices='Not Important', user=request.user).order_by('-pk')

                paginator = Paginator(smth, 4)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)

            return render(request, 'home.html',
                          {'list': smth, 'page_obj': page_obj, 'search': search, 'customer': customer,
                           'allurls_count': allurls_count, 'importanturls_count': importanturls_count,
                           'almostimportanturls_count': almostimportanturls_count,
                           'notimportanturls_count': notimportanturls_count})
        else:

            return render(request, 'home.html')


class Create(View):

    def get(self, request):
        forms = UrlForm()
        context = {'form': forms}
        return render(request, 'create.html', context)

    def post(self, request):
        forms = UrlForm(request.POST)
        context = {'form': forms}
        if forms.is_valid():
            data = forms.cleaned_data
            about_url = AboutUrl.objects.create(user=request.user, original_url=data['original_url'],
                                                title=data['title'], description=data['description'],
                                                date_published=datetime.now(), choices=data['choices'])
            about_url.save()
            return redirect('home')

        return render(request, 'create.html', context)


class Update(View):
    def get(self, request, pk):
        new_info = AboutUrl.objects.get(pk=pk)
        new_form = UrlForm(instance=new_info)
        return render(request, 'update.html', {'new_form': new_form})

    def post(self, request, pk):
        new_info = get_object_or_404(AboutUrl, pk=pk)
        new_form = UrlForm(request.POST or None,
                           instance=new_info)  # UrlForm(request.POST or None) : I forgot what is happening here
        if new_form.is_valid():
            new_form.save()
            return redirect('home')
        return render(request, 'update.html', {'new_form': new_form})


class Delete(View):
    def get(self, request, pk):
        smth = AboutUrl.objects.get(pk=pk)
        return render(request, 'delete.html', {'smth': smth})

    def post(self, request, pk):
        smth = get_object_or_404(AboutUrl, pk=pk)

        if smth:
            smth.delete()
            return redirect('home')
        return render(request, 'delete.html', {'smth': smth})


class Read(View):
    def get(self, request, pk):
        newone = AboutUrl.objects.get(pk=pk)
        return render(request, 'read.html', {'newone': newone})


class BaseUser(View):
    def get(self, request):
        user = CustomUser.objects.get(email=request.user.email)
        template_name = 'navigation.html'
        context = {'user': user}
        return render(request, template_name, context)


class BaseUserDesc(View):
    def get(self, request):
        user = CustomUser.objects.get(email=request.user.email)
        last_attend = user.last_login
        return render(request, 'user_info.html', {'user': user, 'last_attend': last_attend})


class SignOut(View):
    def get(self, request):
        user = CustomUser.objects.get(email=request.user.email)
        return render(request, 'user_delete.html', {'user': user})

    def post(self, request):
        user = CustomUser.objects.get(email=request.user.email)
        if user:
            user.delete()
            return redirect('home')
        return render(request, 'user_delete.html', {'user': user})


class RoomTemprature(View):
    def get(self, request):
        template = "temprature.html"
        #arduino = serial.Serial('/dev/ttyACM0', timeout=1, baudrate=9600)

        # try:
        #     arduino = serial.Serial('/dev/ttyACM0', timeout=1, baudrate=9600)
        # except:
        #     return render(request, template, {"temprature": [0]})
        # raw_data = ""
        # count = 0
        # while count < 1:
        #     count += 1
        #     if str(arduino.readline()).startswith("0"):
        #         count -= 1
        #         continue
        #     for x in str(arduino.readline()):
        #         if x != ".":
        #             if x.isdigit():
        #                 raw_data += x
        #             else:
        #                 pass
        #         else:
        #             break
        # try:
        #     if int(raw_data) >= 30:
        #         arduino.writelines(b'H')
        #         print("high")
        #     else:
        #         arduino.writelines(b'L')
        #         print("low")
        #     arduino.close()
        # except ValueError:
        #     raw_data = 0

        context = {"temprature": [0, 20], "data": 17}
        return render(request, template, context)
# {% url 'path name' %}
