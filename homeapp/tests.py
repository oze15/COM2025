from urllib import response
from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class HomePageTests(TestCase):
    """Test whether out notes application homepage works"""
    @classmethod
    def setUp(self):
        # Will be used to do any set up before test cases
        return
    
    # def test_contact(self):
    #     response = self.client.get(reverse('contact'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'This is my header')
    #     self.assertContains(response, 'Contact Us')
    #     self.assertContains(response, 'This is my footer')

#   Logged out tests
    # Can I see the jumbotron?
    def test_homepage_logged_out(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

        # NAVBAR TEST
        # When there is no logged in user, the tasks link in the navbar should not be shown
        # so if is not seen then we know the logic in the navbar is fine
        self.assertNotContains(response, 'Tasks')
        
        # MAIN BODY TEST
        # This is part of the jumbotron style div that is shown only when not logged in
        self.assertContains(response, 'The only task management solution.')
        # Another part of the jumbotron style div
        self.assertContains(response, 'toDoList is a brand new task management app made for the 21st century human.')
        
        # FOOTER TEST
        # Test 
        self.assertContains(response, 'No account?')
    
    
#   Logged in tests
    def test_homepage_logged_in(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

        # NAVBAR TEST
        # When there is no logged in user, the tasks link in the navbar should not be shown
        # so if is not seen then we know the logic in the navbar is fine
        
        
        # MAIN BODY TEST
        # This is part of the jumbotron style div that is shown only when not logged in
        
        # Another part of the jumbotron style div
        
        # FOOTER TEST
        # Test 