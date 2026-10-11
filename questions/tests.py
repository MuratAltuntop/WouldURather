import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from questions.models import Question, Choice, Vote


class WouldURatherTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="secret_private_email@example.com",
            password="password123"
        )
        self.question = Question.objects.create(
            title="Uçabilmek mi, görünmez olmak mı?",
            author=self.user
        )
        self.choice_a = Choice.objects.create(
            question=self.question,
            choice_text="Uçabilmek",
            votes=5,
            order=1
        )
        self.choice_b = Choice.objects.create(
            question=self.question,
            choice_text="Görünmez olmak",
            votes=5,
            order=2
        )

    def test_focus_view_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Uçabilmek mi, görünmez olmak mı?")
        self.assertContains(response, "@testuser")
        # Ensure email is NEVER exposed
        self.assertNotContains(response, "secret_private_email@example.com")

    def test_feed_view_loads(self):
        response = self.client.get(reverse("feed"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Uçabilmek")
        self.assertContains(response, "Görünmez olmak")
        self.assertNotContains(response, "secret_private_email@example.com")

    def test_anonymous_vote_api(self):
        response = self.client.post(
            reverse("vote", args=[self.choice_a.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["votes_a"], 6)
        self.assertEqual(data["pct_a"], round((6 / 11) * 100))

        # Check that voting again returns already_voted
        response2 = self.client.post(
            reverse("vote", args=[self.choice_b.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        data2 = response2.json()
        self.assertTrue(data2["already_voted"])

    def test_authenticated_vote_and_profile(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            reverse("vote", args=[self.choice_b.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("testuser", data["recent_voters"])
        self.assertNotIn("secret_private_email@example.com", str(data))

        # Check Profile Page
        profile_response = self.client.get(reverse("profile"))
        self.assertEqual(profile_response.status_code, 200)
        self.assertContains(profile_response, "@testuser")
        self.assertContains(profile_response, "Uçabilmek mi, görünmez olmak mı?")
        self.assertNotContains(profile_response, "secret_private_email@example.com")

    def test_create_question_requires_login(self):
        # Anonymous should redirect to login
        response = self.client.get(reverse("create_question"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

        # Authenticated can create
        self.client.login(username="testuser", password="password123")
        post_response = self.client.post(reverse("create_question"), {
            "title": "Çay mı, Kahve mi?",
            "choice_a": "Çay ☕",
            "choice_b": "Kahve ☕",
        })
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(Question.objects.filter(title="Çay mı, Kahve mi?").exists())
