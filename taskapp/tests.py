from django.test import TestCase
from django.db.backends.sqlite3.base import IntegrityError
from django.db import transaction
from .models import Note, Task
from django.urls import reverse
from .forms import TaskForm
from django.contrib.auth.models import User

# Create your tests here.


class NoteTests(TestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     n1 = Note(title='1st Note', description="This is my 1st note")
    #     n1.save()
    #     n2 = Note(title='2nd Note', description="This is my 2nd note")
    #     n2.save()
    # def test_save_note(self):
    #     db_count = Note.objects.all().count()
    #     note = Note(title='new Note', description='New description')
    #     note.save()
    #     self.assertEqual(db_count+1, Note.objects.all().count())
    # def test_duplicate_title(self):
    #     db_count = Note.objects.all().count()
    #     note = Note(title='1st Note', description="This is my 1st note")
    #     #with self.assertRaises(IntegrityError):
    #     try:
    #         with transaction.atomic():
    #             note.save() 
    #     except IntegrityError:
    #         pass
    #     self.assertNotEqual(db_count+1, Note.objects.all().count())

    # def test_post_create(self):
    #     db_count = Note.objects.all().count()
    #     data = {
    #         "title": "new note",
    #         "description": " new description",
    #     }
    #     response = self.client.post(reverse('notes_new'), data=data)
    #     self.assertEqual(Note.objects.count(), db_count+1)

    # # setup and noe tests here
    # def test_post_create_task(self):
    #     note = Note.objects.get(pk=1)
    #     data = {
    #         "title": "new task",
    #         "complete": True,
    #         "note": note
    #     }
        
    #     form = TaskForm(data)
    #     self.assertTrue(form.is_valid())

    # def test_post_create_empty_task(self):
    #     data = {
    #         "title": "",
    #         "complete": True,
    #         "note": Note.objects.get(pk=1)
    #     }
    #     form = TaskForm(data)
    #     self.assertFalse(form.is_valid())

    @classmethod
    # Test that your login works
    def setUpTestData(cls):
        user1 = User(username='user1', email='user1@email.com')
        user1.set_password('MyPassword123')
        user1.save()
        user2 = User(username='user2', email='user2@email.com')
        user2.set_password('MyPassword123')
        user2.save()
        
        n1 = Note(title='1st Note', description="This is my 1st note", author=user1)
        n1.save()
        n2 = Note(title='2nd Note', description="This is my 2nd note", author=user1)
        n2.save()
        
    def test_login(self):
        login = self.client.login(username='user1', password='MyPassword123')
        self.assertTrue(login)

    # Add users to your notes tests
    def test_save_note(self):
        db_count = Note.objects.all().count()
        user1=User.objects.get(pk=1)
        note = Note(title='new Note', description='New description', author=user1)
        note.save()
        self.assertEqual(db_count+1, Note.objects.all().count())

    def test_duplicate_title(self):
        db_count = Note.objects.all().count()
        user1=User.objects.get(pk=1)
        note = Note(title='1st Note', description="This is my 1st note", author=user1)
        #with self.assertRaises(IntegrityError):
        try:
            with transaction.atomic():
                note.save()
        except IntegrityError:
            pass
        self.assertNotEqual(db_count+1, Note.objects.all().count())

    # Test protected urls when logged in and logged out
    def test_post_create_note_no_login(self):
        db_count = Note.objects.all().count()
        user1=User.objects.get(pk=1)
        data = {
            "title": "new note",
            "description": " new description",
            "author": user1
        }
        response = self.client.post(reverse('notes_new'), data=data)
        self.assertEqual(Note.objects.count(), db_count)
    
    def test_post_create_note_with_login(self):
        db_count = Note.objects.all().count()
        user1=User.objects.get(pk=1)
        login = self.client.login(username='user1', password='MyPassword123')
        data = {
            "title": "new note",
            "description": " new description",
            "author": user1
        }
        response = self.client.post(reverse('notes_new'), data=data)
        self.assertEqual(Note.objects.count(), db_count)