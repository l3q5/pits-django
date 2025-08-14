from django.db import models


class Climate(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Terrain(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Planet(models.Model):
    name = models.CharField(max_length=100, unique=True)
    population = models.BigIntegerField(null=True, blank=True)
    climates = models.ManyToManyField(Climate, related_name="planets")
    terrains = models.ManyToManyField(Terrain, related_name="planets")

    def __str__(self):
        return self.name
