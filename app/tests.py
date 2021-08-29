from django.test import TestCase, Client, SimpleTestCase
from .models import CustomUser, AboutUrl
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestRegisterUser(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.email = 'kurbonaliotahonov45@gmail.com'
        self.first_name = 'Salohiddin'
        self.last_name = 'Halimjonov'
        self.gender = 'Male'
        self.password = '123456789ab'

    def test_register_user_url(self):
        response = self.client.get('/register/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/register.html')

    def test_register_page_view_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/register.html')

    def test_register_form(self):
        response = self.client.post(reverse('register'), data={
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': 'Male',
            'password1': '123456789ab',
            'password2': '123456789ab',
        })
        self.assertEqual(response.status_code, 302)#I am using 302 status code. because after I registered it automatically redirects to another page

        users = get_user_model().objects.all()# get_user_model():  This method will return the currently active User model
        self.assertEqual(users.count(), 1)

class TestLoginUser(TestCase):
    def setUp(self) -> None:
        self.client = Client()# it is like new browser
        self.user = CustomUser.objects.create(email='kurbonaliotahonov45@gmail.com', first_name='Salohiddin',
                                              last_name='Halimjonov', gender='Male')
        self.user.set_password('123456789ab')#this is better way than using user_create() function.
        self.user.save()
        #While with the create_user() the username and password are set as given and password will be hashed automatically and
        # the returned User object will have is_active set to True
    def testloginuser(self):
        response = self.client.login(email=self.user.email, password='123456789ab')
        self.assertTrue(response)

class TestLogoutUser(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def testloginuser(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

class TestCreate(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = CustomUser.objects.create(email='kurbonaliotahonov45@gmail.com', first_name='Salohiddin',
                                              last_name='Halimjonov', gender='Male')
        self.user.set_password('123456789ab')  # this is better way than using user_create() function.
        self.user.save()
    def testloginuser(self):
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 200)
        smth = CustomUser.objects.get(first_name='Salohiddin')
        self.assertEqual(smth, self.user)
        self.assertEquals(CustomUser.objects.all().count(), 1)
        self.assertTemplateUsed(response, 'create.html')
class TestUpdate(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def testupdateuser(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update.html')
class TestDelete(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def testdeleteuser(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete.html')


class HomePageTests(SimpleTestCase):

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


    def test_home_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/')
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')



