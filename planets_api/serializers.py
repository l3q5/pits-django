from rest_framework import serializers
from .models import Planet, Climate, Terrain


class PlanetSerializer(serializers.ModelSerializer):
    climates = serializers.StringRelatedField(many=True, read_only=True)
    terrains = serializers.StringRelatedField(many=True, read_only=True)

    climates_input = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    terrains_input = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Planet
        fields = [
            "id",
            "name",
            "population",
            "climates",
            "terrains",
            "climates_input",
            "terrains_input",
        ]

    def create(self, validated_data):
        climates_data = validated_data.pop("climates_input", [])
        terrains_data = validated_data.pop("terrains_input", [])

        planet = Planet.objects.create(**validated_data)

        for climate_name in climates_data:
            climate, _ = Climate.objects.get_or_create(name=climate_name)
            planet.climates.add(climate)

        for terrain_name in terrains_data:
            terrain, _ = Terrain.objects.get_or_create(name=terrain_name)
            planet.terrains.add(terrain)

        return planet

    def update(self, instance, validated_data):
        climates_data = validated_data.pop("climates_input", None)
        terrains_data = validated_data.pop("terrains_input", None)

        instance.name = validated_data.get("name", instance.name)
        instance.population = validated_data.get("population", instance.population)
        instance.save()

        if climates_data is not None:
            instance.climates.clear()
            for climate_name in climates_data:
                climate, _ = Climate.objects.get_or_create(name=climate_name)
                instance.climates.add(climate)

        if terrains_data is not None:
            instance.terrains.clear()
            for terrain_name in terrains_data:
                terrain, _ = Terrain.objects.get_or_create(name=terrain_name)
                instance.terrains.add(terrain)

        return instance
