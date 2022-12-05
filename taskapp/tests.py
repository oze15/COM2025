from django.test import TestCase
from django.db.backends.sqlite3.base import IntegrityError
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Task, SubTask, User
from django.urls import reverse
from .forms import TaskForm
# from django.contrib.auth.models import User

# Create your tests here.

class TaskTests(TestCase):

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

        ## Create task 3 for user 1
        task3 = Task(
            title       = '3rd Task',
            description = "This is my 3rd task", 
            author      = user1,
            category    = 'Category 1', 
            status      = 'Not started',
            due_at      = '2021-01-01'
            )
        task3.save()

        ## Create subtask 1 for user 1
        subtask1 = SubTask(
            title       = '1st Task',
            task        = task1
            )
        subtask1.save()

    # Is is possible to login?
    def test_login(self):
        # Attempt to login with given username and password
        login = self.client.login(username = 'user1', password = 'MyPassword123')
        # Was login successful?
        self.assertTrue(login)

    # Is is possible to logout?
    def test_logout(self):
        # Attempt to login with given username and password
        login = self.client.login(username = 'user1', password = 'MyPassword123')
        logout = self.client.logout
        # Was logout successful?
        self.assertTrue(logout)

    # Save a note as a user
    def test_save_task(self):
        # get current count to check for potential change later
        db_count = Task.objects.all().count()
        # get user 1
        user1 = User.objects.get(pk = 1)
        # add a new task to database by user 1
        task = Task(
            title       = 'New Task', 
            description = "This is a new task", 
            author      = user1, 
            category    = 'Category 1', 
            status      = 'Not started', 
            due_at      = '2021-01-01'
            )
        task.save()
        # has the task been added? Will know as number of tasks will increase by 1
        self.assertEqual(db_count + 1, Task.objects.all().count())

    # Attempt to make a task with a duplicate title
    def test_duplicate_title(self):
        # get current count to check for potential change later
        db_count = Task.objects.all().count()
        # get user 1
        user1 = User.objects.get(pk=1)
        # add a new task to database by user 1
        task = Task(
            title       = '1st Task',
            description = "This is my 1st task", 
            author      = user1,
            category    = 'Category 1', 
            status      = 'Not started',
            due_at      = '2021-01-01'
            )
        # attempt to save task
        try:
            with transaction.atomic():
                task.save()
        except IntegrityError:
            pass
        # This shouldn't work so we expect the database to not increase in size by 1,  
        # i.e. it should be the same size as it was before we started to attempt this
        self.assertNotEqual(db_count + 1, Task.objects.all().count())

    # Attempt to make a task with a duplicate title
    def test_invalid_data(self):
        # get user 1
        user1 = User.objects.get(pk=1)
        # add a new task to database by user 1
        task = Task(
            title       = '1st Task',
            description = "This is my 1st task", 
            author      = user1,
            category    = 'Category 1', 
            status      = 'Not started',
            due_at      = '2021-01---'
            )

        self.assertRaises(ValidationError, task.full_clean)

    # Save a note as a user
    # def test_create_task_with_subtasks_and_delete_cascade(self):
    #     # get current count to check for potential change later
    #     db_count = Task.objects.all().count()
    #     # get user 1
    #     user1 = User.objects.get(pk = 1)
    #     # add a new task to database by user 1
    #     task = Task(
    #         title       = 'New Task', 
    #         description = "This is a new task", 
    #         author      = user1, 
    #         category    = 'Category 1', 
    #         status      = 'Not started', 
    #         due_at      = '2021-01-01'
    #         )
    #     task.save()
    #     task.delete
    #     # Add assertions to test that subtasks have been created
    #     # that you can't find the subtasks on delete when you have
    #     # deleted the task 
    #     # -> this it to test on_delete = models.CASCADE holds
    #     self.assertEqual(db_count, Task.objects.all().count())

    # Save a note as a user
    # def test_create_task_with_author_then_delete_author(self):
    #     # get current count to check for potential change later
    #     db_count = Task.objects.all().count()
    #     # get user 1
    #     user1 = User.objects.get(pk = 1)
    #     # add a new task to database by user 1
    #     task = Task(
    #         title       = 'New Task', 
    #         description = "This is a new task", 
    #         author      = user1, 
    #         category    = 'Category 1', 
    #         status      = 'Not started', 
    #         due_at      = '2021-01---'
    #         )
    #     task.full_clean
    #     task.save()
    #     task.delete
    #     # Add assertions to test that subtasks have been created
    #     # that you can't find the subtasks on delete when you have
    #     # deleted the task 
    #     # -> this it to test on_delete = models.CASCADE holds
    #     self.assertEqual(db_count, Task.objects.all().count())


    # Tesk task index view logged in as user/admin
    # def test_toggle_complete_subtask_with_login_as_user(self):
    #     # get current count to check for potential change later
    #     db_count = SubTask.objects.all().count()

    #     self.assertEqual(SubTask.objects.count(), db_count)

# Test protected urls when logged in and logged out

    # What happens when we try to create a task when we haven't logged in?
    def test_post_create_task_no_login(self):
        # get current count to check for potential change later
        db_count = Task.objects.all().count()
        # get user 1
        user1 = User.objects.get(pk = 1)
        # data for a new task with no user but as user 1
        data = {
            "title":        "new task",
            "description":  "new description",
            "author":       user1.id,
            "category":     'Category 1', 
            "status":       'Not started',
            "due_at":       '2021-01-01'
        }
        response = self.client.post(reverse('tasks_new'), data=data)
        self.assertEqual(Task.objects.count(), db_count)
    
    # What happens when we try to create a task when we have logged in?
    def test_post_create_task_with_login(self):
        # get current count to check for potential change later
        db_count = Task.objects.all().count()
        # get user 1
        user1 = User.objects.get(pk = 1)
        # Login with username and password as user 1
        login = self.client.login(username='user1', password='MyPassword123')
        # data for a new task with and as user 1
        data = {
            "title":        "new task",
            "description":  "new description",
            "author":       user1.id,
            "category":     'Category 1', 
            "status":       'Not started',
            "due_at":       '2021-01-01'
        }
        response = self.client.post(reverse('tasks_new'), data=data)
        self.assertEqual(Task.objects.count(), db_count+1)

    def test_read_task_as_user(self):
        # get user 2
        user1 = User.objects.get(pk = 1)
        # Login with username and password as user 2
        login = self.client.login(username='user1', password='MyPassword123')
        # Attempt to read a task belonging to user 1
        response = self.client.get('/tasks/1')
        # Should get task page
        self.assertEqual(response.status_code, 200)

    def test_read_task_as_another_user(self):
        # get user 2
        user2 = User.objects.get(pk = 2)
        # Login with username and password as user 2
        login = self.client.login(username='user2', password='MyPassword123')
        # Attempt to read a task belonging to user 1
        response = self.client.get('/tasks/1')
        # Should get permission denied
        self.assertEqual(response.status_code, 403)

    def test_read_task_no_login(self):
        # Attempt to read a task belonging to user 1
        response = self.client.get('/tasks/1')
        # Should be prompted to login
        self.assertEqual(response.status_code, 302)

    # What happens when we try to create a task when we haven't logged in?
    def test_post_update_task_no_login(self):
        # get current count to check for potential change later
        db_count = Task.objects.all().count()
        # get user 1
        user1 = User.objects.get(pk = 1)
        # data for a new task with no user but as user 1
        data = {
            "title":        "new task",
            "description":  "new description",
            "author":       user1.id,
            "category":     'Category 1', 
            "status":       'Not started',
            "due_at":       '2022-01-01'
        }
        response = self.client.post('/tasks/edit/1', data=data)
        # Won't work as redirects to login page
        self.assertEqual(response.status_code, 302)
        # Is it possible to get the page that the client can
        # currently see? - should be.
    
    # What happens when we try to update a task when we have 
    # logged in as the author of that task (user who created it)?
    def test_post_update_task_with_login_as_user(self):
        # get user 1
        user1 = User.objects.get(pk = 1)
        # Login with username and password as user 1
        login = self.client.login(username='user1', password='MyPassword123')
        # data for a new task with and as user 1
        data = {
            "title":        "new task",
            "description":  "new description",
            "author":       user1.id,
            "category":     'Category 1', 
            "status":       'Not started',
            "due_at":       '2022-01-01'
        }
        response = self.client.post('/tasks/edit/1', data=data)
        # Expected. How about checking for the modified content
        # on the page?
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/tasks/1')
        self.assertContains(response, 'new description')


    # What happens when we try to update a task when we have 
    # logged in as a user who didn't create it?
    def test_post_update_task_with_login_as_another_user(self):
        # get user 1
        user1 = User.objects.get(pk = 1)
        # Login with username and password as user 1
        login = self.client.login(username='user2', password='MyPassword123')
        # data for a new task with and as user 1
        data = {
            "title":        "new task",
            "description":  "new description",
            "author":       user1.id,
            "category":     'Category 1', 
            "status":       'Not started',
            "due_at":       '2022-01-01'
        }
        response = self.client.post('/tasks/edit/1', data=data)
        # Expected. How about checking for the modified content
        # on the page?
        self.assertEqual(response.status_code, 403)

        response = self.client.get('/tasks/1')
        self.assertEqual(response.status_code, 403)

    def test_delete_task_with_login_as_another_user(self):
        # get current count to check for potential change later
        db_count = Task.objects.all().count()
        # get user 2
        user2 = User.objects.get(pk = 2)
        # Login with username and password as user 2
        login = self.client.login(username='user2', password='MyPassword123')
        # Attempt to read a task belonging to user 1
        response = self.client.get('/tasks/delete/1')
        # Should get permission denied
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Task.objects.count(), db_count)

    def test_delete_task_no_login(self):
        # get current count to check for potential change later
        db_count = Task.objects.all().count()
        # Attempt to read a task belonging to user 1
        response = self.client.get('/tasks/delete/1')
        # Should be prompted to login
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), db_count)

    def test_delete_task_with_login_as_user(self):
        # get current count to check for potential change later
        db_count = Task.objects.all().count()
        # get user 1
        user1 = User.objects.get(pk = 1)
        # Login with username and password as user 1
        login = self.client.login(username='user1', password='MyPassword123')
        # Attempt to read a task belonging to user 1
        response = self.client.get('/tasks/delete/1')
        # Should get task page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), db_count-1)

    # Create a subtask logged in/out/as another user

    def test_post_create_subtask_with_login_as_user(self):
        # get current count to check for potential change later
        db_count = SubTask.objects.all().count()
        task = Task.objects.get(id = 1)
        # Login with username and password as user 1
        login = self.client.login(username='user1', password='MyPassword123')
        # Attempt to make a subtask belonging to user 1
        data = {
            "title":        "new task",
            "complete":     False,
            "task":         task.id
        }
        response = self.client.post('/tasks/1/subtask/new', data=data)

        self.assertEqual(SubTask.objects.count(), db_count+1)

    def test_post_create_subtask_with_login_as_another_user(self):
        # get current count to check for potential change later
        db_count = SubTask.objects.all().count()
        task = Task.objects.get(id = 1)
        # Login with username and password as user 2
        login = self.client.login(username='user2', password='MyPassword123')
        # Attempt to make a subtask belonging to userS 1
        data = {
            "title":        "new task",
            "complete":     False,
            "task":         task.id
        }
        response = self.client.post('/tasks/1/subtask/new', data=data)

        self.assertEqual(SubTask.objects.count(), db_count)

    def test_post_create_subtask_no_login(self):
        # get current count to check for potential change later
        db_count = SubTask.objects.all().count()
        task = Task.objects.get(id = 1)
        # Attempt to make a subtask belonging to user 1
        data = {
            "title":        "new task",
            "complete":     False,
            "task":         task.id
        }
        response = self.client.post('/tasks/1/subtask/new', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SubTask.objects.count(), db_count)

    # Toggle complete logged in/out/as another user
    def test_toggle_complete_subtask_with_login_as_user(self):
        # Login with username and password as user 1
        login = self.client.login(username='user1', password='MyPassword123')
        
        # Attempt to toggle a subtask belonging to user 1
        response = self.client.get('/tasks/togglecomplete?subtask_id=1')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '{"complete": true, "tid": "1"}')

        response = self.client.get('/tasks/togglecomplete?subtask_id=1')
        self.assertContains(response, '{"complete": false, "tid": "1"}')

    def test_toggle_complete_subtask_with_login_as_another_user(self):
        # Login with username and password as user 2
        login = self.client.login(username='user2', password='MyPassword123')

        # Attempt to toggle a subtask belonging to user 1
        response = self.client.get('/tasks/togglecomplete?subtask_id=1')

        # Should get permission denied
        self.assertEqual(response.status_code, 403)        

    def test_toggle_complete_subtask_no_login(self):
        # Attempt to toggle a subtask belonging to user 1
        response = self.client.get('/tasks/togglecomplete?subtask_id=1')
        # Should be prompted to login
        self.assertEqual(response.status_code, 302)

    # Delete subtask logged in/out/as another user
    def test_delete_subtask_with_login_as_user(self):
        # get current count to check for potential change later
        db_count = SubTask.objects.all().count()

        # Login with username and password as user 1
        login = self.client.login(username='user1', password='MyPassword123')
        
        # Attempt to delete a subtask belonging to user 1
        response = self.client.get('/tasks/deletesubtask?subtask_id=1')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '{"delete_success": true, "tid": "1"}')
        self.assertEqual(SubTask.objects.count(), db_count-1)

    def test_delete_subtask_with_login_as_another_user(self):
        # get current count to check for potential change later
        db_count = SubTask.objects.all().count()

        # Login with username and password as user 1
        login = self.client.login(username='user2', password='MyPassword123')
        
        # Attempt to delete a subtask belonging to user 1
        response = self.client.get('/tasks/deletesubtask?subtask_id=1')

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(SubTask.objects.count(), db_count-1)

    def test_delete_subtask_no_login(self):
        # get current count to check for potential change later
        db_count = SubTask.objects.all().count()

        # Attempt to delete a subtask belonging to user 1
        response = self.client.get('/tasks/deletesubtask?subtask_id=1')

        # Should be prompted to login
        self.assertEqual(response.status_code, 302)

        self.assertEqual(SubTask.objects.count(), db_count)