"""Unit and integration tests for the calorie tracking app."""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Food, Consume


class FoodModelTest(TestCase):
    """Tests for the Food model."""

    def test_create_food(self):
        """Test that a food item is created correctly."""
        food = Food.objects.create(name="Banana", carbs=20, protein=1, fats=0, calories=90)  # pylint: disable=no-member
        self.assertEqual(food.name, "Banana")
        self.assertEqual(food.carbs, 20)
        self.assertEqual(food.protein, 1)
        self.assertEqual(food.fats, 0)
        self.assertEqual(food.calories, 90)


class ConsumeModelTest(TestCase):
    """Tests for the Consume model."""

    def setUp(self):
        """Create a test user and food."""
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.food = Food.objects.create(name="Orange", carbs=15, protein=1, fats=0, calories=60)  # pylint: disable=no-member

    def test_create_consume(self):
        """Test that a Consume record links user and food correctly."""
        consume = Consume.objects.create(user=self.user, food_consumed=self.food)  # pylint: disable=no-member
        self.assertEqual(consume.food_consumed.name, "Orange")
        self.assertEqual(consume.user.username, "testuser")


class IndexViewTest(TestCase):
    """Tests for index view behavior."""

    def setUp(self):
        """Set up user and food for tests."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.food = Food.objects.create(name="Rice", carbs=28, protein=3, fats=0, calories=130)  # pylint: disable=no-member

    def test_redirect_if_not_logged_in(self):
        """Test that unauthenticated user is redirected."""
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/admin/login/?next=/')

    def test_logged_in_uses_correct_template(self):
        """Test that logged in user sees correct template."""
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/index.html')

    def test_add_food_post(self):
        """Test adding a food via POST adds a record."""
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('index'), {'food_consumed': self.food.name})
        self.assertEqual(Consume.objects.count(), 1)  # pylint: disable=no-member
        consume = Consume.objects.first()  # pylint: disable=no-member
        self.assertEqual(consume.food_consumed.name, "Rice")
        self.assertEqual(consume.user.username, "testuser")


class DeleteConsumeTest(TestCase):
    """Tests for deleting consumed food."""

    def setUp(self):
        """Set up user and one consume record."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.food = Food.objects.create(name="Chicken", carbs=0, protein=30, fats=3, calories=165)  # pylint: disable=no-member
        self.consume = Consume.objects.create(user=self.user, food_consumed=self.food)  # pylint: disable=no-member

    def test_redirect_if_not_logged_in(self):
        """Test redirect when user is not logged in."""
        response = self.client.get(reverse('delete', args=[self.consume.id]))
        self.assertRedirects(response, f'/admin/login/?next=/delete/{self.consume.id}/')

    def test_logged_in_delete_food(self):
        """Test that food is deleted successfully."""
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('delete', args=[self.consume.id]))
        self.assertEqual(Consume.objects.count(), 0)  # pylint: disable=no-member

    def test_delete_page_loads(self):
        """Test that the delete confirmation page loads."""
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('delete', args=[self.consume.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/delete.html')


class ExtendedTests(TestCase):
    """Additional frontend-related tests."""

    def setUp(self):
        """Set up test data and login user."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.food = Food.objects.create(name="Pasta", carbs=30, protein=6, fats=1, calories=150)  # pylint: disable=no-member
        self.client.login(username='testuser', password='12345')

    def test_add_multiple_food_items(self):
        """Test that two different food items are added."""
        food2 = Food.objects.create(name="Salad", carbs=5, protein=1, fats=0, calories=25)  # pylint: disable=no-member
        self.client.post(reverse('index'), {'food_consumed': self.food.name})
        self.client.post(reverse('index'), {'food_consumed': food2.name})
        self.assertEqual(Consume.objects.count(), 2)  # pylint: disable=no-member

    def test_add_nonexistent_food(self):
        """Test that adding invalid food redirects instead of crashing."""
        response = self.client.post(reverse('index'), {'food_consumed': 'NonexistentFood'})
        self.assertEqual(response.status_code, 302)

    def test_delete_nonexistent_consume(self):
        """Test that deleting non-existent item redirects."""
        response = self.client.post(reverse('delete', args=[999]))
        self.assertEqual(response.status_code, 302)

    def test_progress_bar_updates(self):
        """Test that progress bar is rendered."""
        self.client.post(reverse('index'), {'food_consumed': self.food.name})
        response = self.client.get(reverse('index'))
        self.assertContains(response, "progress-bar")

class AdditionalTests(TestCase):
    """Extra tests for frontend structure and logic validation."""

    def setUp(self):
        """Set up client and test user."""
        self.client = Client()
        self.user = User.objects.create_user(username='extrauser', password='12345')
        self.client.login(username='extrauser', password='12345')
        self.food = Food.objects.create(name="Milk", carbs=12, protein=8, fats=5, calories=120)  # pylint: disable=no-member

    def test_table_headers_present(self):
        """Check if table headers are rendered on the page."""
        response = self.client.get(reverse('index'))
        self.assertContains(response, "Food item")
        self.assertContains(response, "Calories(Kcal)")

    def test_duplicate_food_addition(self):
        """Test that user can add same food multiple times."""
        self.client.post(reverse('index'), {'food_consumed': self.food.name})
        self.client.post(reverse('index'), {'food_consumed': self.food.name})
        self.assertEqual(Consume.objects.count(), 2)  # pylint: disable=no-member

    def test_other_user_food_not_visible(self):
        """Ensure one user does not see another user's consumed food."""
        other_user = User.objects.create_user(username='otheruser', password='12345')
        Consume.objects.create(user=other_user, food_consumed=self.food)  # pylint: disable=no-member
        response = self.client.get(reverse('index'))
        # Перевірка — чи є слово "Milk" саме в таблиці спожитої їжі
        table_section = response.content.decode().split("Today's Consumption")[1]
        self.assertNotIn("Milk", table_section)

    def test_empty_table_handling(self):
        """Test that page works with no consumed food records."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Total")

    def test_delete_button_shows(self):
        """Test that delete button is present in table."""
        Consume.objects.create(user=self.user, food_consumed=self.food)  # pylint: disable=no-member
        response = self.client.get(reverse('index'))
        self.assertContains(response, "Remove Item")

    def test_navigation_bar_present(self):
        """Test that navbar is rendered correctly."""
        response = self.client.get(reverse('index'))
        self.assertContains(response, "Calorie Tracker")
        self.assertContains(response, "Home")

    def test_csrf_protection_enabled(self):
        """Ensure CSRF token is present in form."""
        response = self.client.get(reverse('index'))
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_food_appears_in_dropdown(self):
        """Test that added food appears in the <select> dropdown menu."""
        response = self.client.get(reverse('index'))
        self.assertContains(response, f'<option value="{self.food.name}">{self.food.name}</option>')



