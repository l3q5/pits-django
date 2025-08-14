import requests
from django.core.management.base import BaseCommand
from planets_api.models import Planet, Climate, Terrain


class Command(BaseCommand):
    help = (
        "Fetches planet data from the SWAPI GraphQL endpoint and populates the database"
    )

    def handle(self, *args, **options):
        graphql_endpoint = "https://swapi-graphql.netlify.app/graphql"
        query = """
        query Query {
            allPlanets {
                planets {
                    name
                    population
                    terrains
                    climates
                }
            }
        }
        """

        self.stdout.write("Fetching data from SWAPI...")
        response = requests.post(graphql_endpoint, json={"query": query})

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR("Failed to fetch data."))
            return

        data = response.json()
        planets_data = data.get("data", {}).get("allPlanets", {}).get("planets", [])

        if not planets_data:
            self.stdout.write(self.style.WARNING("No planets found in the response."))
            return

        for planet_data in planets_data:
            population = planet_data.get("population")
            if population == "unknown":
                population = None

            planet, created = Planet.objects.update_or_create(
                name=planet_data["name"], defaults={"population": population}
            )

            climates_list = planet_data.get("climates")
            if climates_list:
                for climate_name in climates_list:
                    climate, _ = Climate.objects.get_or_create(name=climate_name)
                    planet.climates.add(climate)

            terrains_list = planet_data.get("terrains")
            if terrains_list:
                for terrain_name in terrains_list:
                    terrain, _ = Terrain.objects.get_or_create(name=terrain_name)
                    planet.terrains.add(terrain)

            status = "Created" if created else "Updated"
            self.stdout.write(
                self.style.SUCCESS(f"Successfully {status} planet: {planet.name}")
            )

        self.stdout.write(self.style.SUCCESS("Database population complete."))
