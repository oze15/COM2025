from urllib import response
from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class HomePageTests(TestCase):
    """Test whether out notes application homepage works"""

    def setUp(self):
        # Will be used to do any set up before test cases
        return

# # fix these tests
#     def test_homepage(self):
#         response = self.client.get('')
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'This is My Home Page')
#         self.assertContains(response, 'This is my footer')
    
#     def test_contact(self):
#         response = self.client.get(reverse('contact'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'This is my header')
#         self.assertContains(response, 'Contact Us')
#         self.assertContains(response, 'This is my footer')
