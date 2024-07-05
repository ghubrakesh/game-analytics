from django.test import TestCase, Client
from django.urls import reverse
from .models import GameData
from datetime import datetime
import json


# Create your tests here.
class GameDataTests(TestCase):
    """
    This test case will create a new GameData object, and test it among various cases.
    Test case will fail if anything written in code does not make sense.
    """
    def setUp(self):
        self.client = Client()
        self.upload_url = reverse('upload_csv')
        self.query_url = reverse('query_data')
        self.game_data = GameData.objects.create(
            app_id=1,
            name="Test Game",
            release_date=datetime.strptime("Jan 1, 2020", '%b %d, %Y'),
            required_age=18,
            price=29.99,
            dlc_count=2,
            about_the_game="This is a test game.",
            supported_languages="English, Spanish",
            windows=True,
            mac=False,
            linux=True,
            positive=100,
            negative=10,
            score_rank=1,
            developers=json.dumps(["Developer 1", "Developer 2"]),
            publishers=json.dumps(["Publisher 1"]),
            categories=json.dumps(["Category 1"]),
            genres=json.dumps(["Action", "Adventure"]),
            tags=json.dumps(["Tag 1", "Tag 2"])
        )

    def test_upload_csv(self):
        test_url = "https://docs.google.com/spreadsheets/d/asfh/edit?usp=sharing"
        response = self.client.post(self.upload_url, {'csv_url': test_url})
        self.assertEqual(response.status_code, 404)  # Redirect on success
        self.assertEqual(GameData.objects.count(), 1)  # Check if data is inserted

    def test_query_data(self):
        response = self.client.get(self.query_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Game")
        self.assertContains(response, "2020-01-01")
        self.assertContains(response, "29.99")

    def test_filter_query(self):
        data = {
            'name': 'Test',
            'price': 29.99,
            'price_context': 'eq',
            'required_age': 18,
            'age_context': 'eq'
        }
        response = self.client.post(self.query_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Game")

    def test_game_detail_view(self):
        import pdb;pdb.set_trace()
        detail_url = reverse('game_detail', args=[self.game_data.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Game")
        self.assertContains(response, "<label>Available on Mac:</label> No")
        self.assertContains(response, "<label>Available on Windows:</label> Yes")
        self.assertContains(response, "<label>Available on Windows:</label> Yes")
        self.assertContains(response, "<label>Developers:</label> [&quot;Developer 1&quot;, &quot;Developer 2&quot;]")
        self.assertContains(response, "<label>Publishers:</label> [&quot;Publisher 1&quot;]")
        self.assertContains(response, "<label>Categories:</label> [&quot;Category 1&quot;]")
        self.assertContains(response, "><label>Genres:</label> [&quot;Action&quot;, &quot;Adventure&quot;]")
        self.assertContains(response, "<label>Tags:</label> [&quot;Tag 1&quot;, &quot;Tag 2&quot;]")

