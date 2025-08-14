import requests
from unittest.mock import patch, Mock
from django.urls import reverse
from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Planet, Climate, Terrain

MOCK_SWAPI_RESPONSE = {
    "data": {
        "allPlanets": {
            "planets": [
                {
                    "name": "Tatooine",
                    "population": "200000",
                    "terrains": ["desert"],
                    "climates": ["arid"],
                },
                {
                    "name": "Alderaan",
                    "population": "2000000000",
                    "terrains": ["grasslands", "mountains"],
                    "climates": ["temperate"],
                },
                {
                    "name": "Hoth",
                    "population": None,
                    "terrains": ["tundra", "ice caves", "mountain ranges"],
                    "climates": ["frozen", "murky"],
                },
            ]
        }
    }
}


class ManagementCommandTest(APITestCase):
    @patch("requests.post")
    def test_fetch_planets_command_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_SWAPI_RESPONSE
        mock_post.return_value = mock_response

        call_command("fetch_planets")

        self.assertEqual(Planet.objects.count(), 3)
        self.assertEqual(Climate.objects.count(), 4)
        self.assertEqual(Terrain.objects.count(), 6)

        tatooine = Planet.objects.get(name="Tatooine")
        self.assertEqual(tatooine.population, 200000)
        self.assertEqual(tatooine.climates.first().name, "arid")
        self.assertEqual(tatooine.terrains.first().name, "desert")

        alderaan = Planet.objects.get(name="Alderaan")
        self.assertEqual(alderaan.climates.count(), 1)
        self.assertEqual(alderaan.terrains.count(), 2)
        self.assertListEqual(
            list(alderaan.terrains.all().values_list("name", flat=True)),
            ["grasslands", "mountains"],
        )


class PlanetAPITest(APITestCase):
    def setUp(self):
        self.climate1 = Climate.objects.create(name="arid")
        self.climate2 = Climate.objects.create(name="temperate")
        self.terrain1 = Terrain.objects.create(name="desert")
        self.terrain2 = Terrain.objects.create(name="grasslands")

        self.planet1 = Planet.objects.create(name="Tatooine", population=200000)
        self.planet1.climates.add(self.climate1)
        self.planet1.terrains.add(self.terrain1)

        self.planet2 = Planet.objects.create(name="Alderaan", population=2000000000)
        self.planet2.climates.add(self.climate2)
        self.planet2.terrains.add(self.terrain2)

        self.list_url = reverse("planet-list")
        self.detail_url = reverse("planet-detail", kwargs={"pk": self.planet1.pk})

    def test_list_planets(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], "Alderaan")
        self.assertEqual(response.data[1]["name"], "Tatooine")
        self.assertIn("arid", response.data[1]["climates"])

    def test_retrieve_planet(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Tatooine")
        self.assertEqual(response.data["population"], 200000)

    def test_create_planet(self):
        payload = {
            "name": "Naboo",
            "population": 4500000000,
            "climates_input": ["temperate", "moist"],
            "terrains_input": ["grassy hills", "swamps", "forests"],
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Planet.objects.count(), 3)

        naboo = Planet.objects.get(name="Naboo")
        self.assertEqual(naboo.population, 4500000000)
        self.assertEqual(naboo.climates.count(), 2)
        self.assertEqual(naboo.terrains.count(), 3)
        self.assertTrue(Climate.objects.filter(name="moist").exists())

    def test_update_planet_put(self):
        payload = {
            "name": "Tatooine II",
            "population": 300000,
            "climates_input": ["super arid"],
            "terrains_input": ["desert", "rock"],
        }
        response = self.client.put(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.planet1.refresh_from_db()
        self.assertEqual(self.planet1.name, "Tatooine II")
        self.assertEqual(self.planet1.population, 300000)
        self.assertEqual(self.planet1.climates.count(), 1)
        self.assertEqual(self.planet1.climates.first().name, "super arid")
        self.assertEqual(self.planet1.terrains.count(), 2)

    def test_update_planet_patch(self):
        payload = {"population": 250000}
        response = self.client.patch(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.planet1.refresh_from_db()
        self.assertEqual(self.planet1.population, 250000)
        self.assertEqual(self.planet1.name, "Tatooine")

    def test_delete_planet(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Planet.objects.count(), 1)
        self.assertFalse(Planet.objects.filter(pk=self.planet1.pk).exists())
