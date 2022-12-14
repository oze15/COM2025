from urllib import response
from django.test import TestCase
from taskapp.models import Task, SubTask, User
from django.urls import reverse
from django.core import mail

# Create your tests here.
class HomePageTests(TestCase):
    """Test whether out notes application homepage works"""
    @classmethod
    def setUpTestData(cls):

        # Create users

        ## Create user 1
        user1 = User(
            username    = 'user1', 
            email       = 'user1@email.com'
            )
        user1.set_password('MyPassword123')
        user1.save()

        ## Create user 2
        user2 = User(
            username    = 'user2', 
            email       = 'user2@email.com'
            )
        user2.set_password('MyPassword123')
        user2.save()
        
        # Create tasks

        ## Create task 1 for user 1
        task1 = Task(
            title       = '1st Task',
            description = "This is my 1st task", 
            author      = user1,
            category    = 'Category 1', 
            status      = 'Not started',
            due_at      = '2021-01-01'
            )
        # Date needs to be in format YYYY-MM-DD for tests
        task1.save()

        ## Create task 2 for user 1
        task2 = Task(
            title       = '2nd Task',
            description = "This is my 2nd task", 
            author      = user1,
            category    = 'Category 1', 
            status      = 'Not started',
            due_at      = '2021-01-01'
            )
        task2.save()

    # Can I see the "jumbotron"?
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
        # Test that the right footer information is shown when there isn't a user logged in
        self.assertContains(response, 'No account?')
    
    def test_homepage_logged_in(self):
        login = self.client.login(username = 'user1', password = 'MyPassword123')
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        # NAVBAR TEST
        # When there is a logged in user, the tasks link in the navbar should be shown
        self.assertContains(response, 'Tasks')
        # MAIN BODY TEST
        # This is part of the jumbotron style div that is shown only when not logged in
        # so we test here that we can't see it if logged in
        self.assertNotContains(response, 'The only task management solution.')
        self.assertContains(response, 'Delayed')
        # FOOTER TEST
        # Test that the right footer information is shown when there is a logged in user
        # we know the logic is correct, as the following phrase will be in the footer
        self.assertContains(response, 'Logged in as user1')

    def test_contact(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        # NAVBAR TEST
        # Check navbar is shown on feedback page
        self.assertContains(response, 'Home')
        # Test that contact.html main body is shown
        self.assertContains(response, 'Send Feedback')
        # Test that form is rendered correctly
        self.assertContains(response, 'What would you like to change?')
        # FOOTER TEST
        # Test that footer is shown on contact page
        self.assertContains(response, 'toDoList v0.0.1')

    def test_mailer_valid(self):
        # get current count to check for potential change later
        m_count = len(mail.outbox)

        data = {
            "name":         "Alice Bob",
            "subject":      "A message through the mailer",
            "email":        "hello@world.com",
            "message":      "Hello world!"
        }
        
        response = self.client.post(reverse('contact'), data=data, follow=True)
        self.assertContains(response, 'Message Sent')
        self.assertIn("Hello world!", mail.outbox[0].body)
        self.assertEqual(len(mail.outbox), m_count + 1)

    def test_mailer_invalid(self):
        # get current count to check for potential change later
        m_count = len(mail.outbox)

        data = {
            "name":         "Alice Bob",
            "subject":      "A message through the mailer",
            "email":        "hello@world",
            "message":      "Hello world!"
        }
        
        response = self.client.post(reverse('contact'), data=data, follow=True)
        self.assertContains(response, 'Invalid Form Data; Message Not Sent')
        self.assertNotEqual(len(mail.outbox), m_count + 1)