from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from simple_content.views import ContentViewSet, NavigationView
from simple_content.models import Content
from rest_framework.test import force_authenticate
from pytils.translit import slugify


class SimpleContentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='user1',
            is_staff=True,
            is_superuser=True
        )
        self.user.set_password('passW0rdForUser1#')

    def test_get(self):
        factory = APIRequestFactory()
        url = '/content_api/contents/'
        title = 'Sample content'
        content_text = 'Sample content text'
        data = {
            'title': title,
            'content': content_text
        }
        request = factory.post(url, data)
        view = ContentViewSet.as_view({'post': 'create'})
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertIsNotNone(response.data.get('pk'))
        self.assertEqual(response.data.get('slug'), slugify(title))
        content = Content.objects.get(title=title)
        self.assertEqual(content.content, content_text)

        request = factory.get(url, data)
        view = ContentViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 403)


    def test_post(self):
        factory = APIRequestFactory()
        url = '/content_api/contents/'
        title = 'Sample content'
        content_text = 'Sample content text'
        data = {
            'title': title,
            'content': content_text
        }
        request = factory.post(url, data)
        view = ContentViewSet.as_view({'post': 'create'})
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertIsNotNone(response.data.get('pk'))
        self.assertEqual(response.data.get('slug'), slugify(title))
        content = Content.objects.get(title=title)
        self.assertEqual(content.content, content_text)

    def test_update(self):
        factory = APIRequestFactory()
        url = '/content_api/contents/'
        title = 'Sample content'
        content_text = 'Sample content text'
        data = {
            'title': title,
            'content': content_text
        }
        request = factory.post(url, data)
        view = ContentViewSet.as_view({'post': 'create'})
        force_authenticate(request, user=self.user)
        response = view(request)
        content_pk = response.data.get('pk')
        self.assertIsNotNone(content_pk)
        self.assertEqual(response.data.get('slug'), slugify(title))
        content = Content.objects.get(title=title)
        self.assertEqual(content.content, content_text)


        url = '/content_api/contents/{}/'.format(content_pk)
        old_slug = slugify(title)
        title = 'New title'
        content_text = 'New text'
        data = {
            'title': title,
            'content': content_text
        }
        request = factory.put(url, data)
        view = ContentViewSet.as_view({'put': 'update'})
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        self.assertEqual(response.data.get('pk'), content_pk)
        self.assertEqual(response.data.get('slug'), old_slug)
        self.assertNotEqual(response.data.get('slug'), slugify(title))
        content = Content.objects.get(title=title)
        self.assertEqual(content.content, content_text)

    def test_delete(self):
        factory = APIRequestFactory()
        url = '/content_api/contents/'
        title = 'Sample content'
        content_text = 'Sample content text'
        data = {
            'title': title,
            'content': content_text
        }
        request = factory.post(url, data)
        view = ContentViewSet.as_view({'post': 'create'})
        force_authenticate(request, user=self.user)
        response = view(request)
        content_pk = response.data.get('pk')
        self.assertIsNotNone(content_pk)
        self.assertEqual(response.data.get('slug'), slugify(title))
        content = Content.objects.get(title=title)
        self.assertEqual(content.content, content_text)

        url = '/content_api/contents/{}/'.format(content_pk)
        request = factory.delete(url, data)
        view = ContentViewSet.as_view({'delete': 'destroy'})
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        self.assertIsNone(response.data)
        with self.assertRaises(Content.DoesNotExist):
            Content.objects.get(pk=content_pk)


    def test_navigation(self):
        factory = APIRequestFactory()
        url = '/content_api/contents/'
        title = 'Sample content'
        content_text = 'Sample content text'
        data = {
            'title': title,
            'content': content_text
        }
        request = factory.post(url, data)
        view = ContentViewSet.as_view({'post': 'create'})
        force_authenticate(request, user=self.user)
        response = view(request)
        parent_pk = response.data.get('pk')
        self.assertIsNotNone(parent_pk)
        child_title = 'Sample child content'
        child_content_text = 'Sample content text for child'
        data = {
            'title': child_title,
            'content': child_content_text,
            'parent': parent_pk
        }
        request = factory.post(url, data)
        force_authenticate(request, user=self.user)
        response = view(request)
        child_pk = response.data.get('pk')
        navigation_view = NavigationView.as_view()
        request = factory.get(reverse('content_api:navigation_roots'))
        force_authenticate(request, user=self.user)
        response = navigation_view(request)
        self.assertEqual(len(response.data), 1)
        self.assertListEqual(response.data[0].get('children'), [])

        request = factory.get(reverse('content_api:navigation', kwargs={'current': parent_pk}))
        force_authenticate(request, user=self.user)
        response = navigation_view(request, current=parent_pk)
        self.assertEqual(len(response.data[0].get('children')), 1)
        self.assertEqual(response.data[0].get('children')[0].get('pk'), child_pk)




