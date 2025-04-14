from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# ----------------------------
# Language Model
# ----------------------------
class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)  # e.g., 'en', 'hi', 'sa'
    name = models.CharField(max_length=50)  # e.g., English, Hindi, Sanskrit

    def __str__(self):
        return self.name


# ----------------------------
# Alias Model
# ----------------------------
class Alias(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    # Generic relation to associate with any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"{self.name} ({self.language.code})"


# ----------------------------
# Planet Model
# ----------------------------
class Planet(models.Model):
    name = models.CharField(max_length=20, unique=True)
    aliases = GenericRelation(Alias)

    is_visible = models.BooleanField(default=True)
    is_inner = models.BooleanField(default=True)
    is_lagna = models.BooleanField(default=False)
    is_shadow = models.BooleanField(default=False)
    is_dasa = models.BooleanField(default=False)
    is_karaka = models.BooleanField(default=False)
    is_malefic = models.BooleanField(default=False)
    is_benefic = models.BooleanField(default=False)
    is_rajayog = models.BooleanField(default=False)
    is_dhanayog = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# ----------------------------
# Nakshatra Model
# ----------------------------
class Nakshatra(models.Model):
    name = models.CharField(max_length=50)
    aliases = GenericRelation(Alias)
    lord = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


# ----------------------------
# Element (Tatva) Model
# ----------------------------
class Element(models.Model):
    name = models.CharField(max_length=20, unique=True)
    aliases = GenericRelation(Alias)

    def __str__(self):
        return self.name


# ----------------------------
# Rashi Model
# ----------------------------
class Rashi(models.Model):
    name = models.CharField(max_length=20)
    aliases = GenericRelation(Alias)
    lord = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True)
    element = models.ForeignKey(Element, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


# ----------------------------
# Awastha (Planet Condition)
# ----------------------------
class Awastha(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# ----------------------------
# House (1 to 12)
# ----------------------------
class House(models.Model):
    number = models.IntegerField(unique=True)

    def __str__(self):
        return f"House {self.number}"


# ----------------------------
# User Kundali (D1 / D9)
# ----------------------------
class UserKundali(models.Model):
    CHART_TYPES = (
        ("D1", "Lagna Chart"),
        ("D9", "Navamsa Chart"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chart_type = models.CharField(max_length=5, choices=CHART_TYPES)
    ascendant = models.ForeignKey(Rashi, on_delete=models.SET_NULL, null=True, related_name="ascendants")
    ascendant_lord = models.CharField(max_length=20)
    varna = models.CharField(max_length=50)
    vashya = models.CharField(max_length=50)
    yoni = models.CharField(max_length=50)
    gan = models.CharField(max_length=50)
    nadi = models.CharField(max_length=50)
    charan = models.IntegerField()
    yog = models.CharField(max_length=50)
    karan = models.CharField(max_length=50)
    tithi = models.CharField(max_length=50)
    yunja = models.CharField(max_length=50)
    tatva = models.CharField(max_length=50)
    name_alphabet = models.CharField(max_length=5)
    paya = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.chart_type}"


# ----------------------------
# Planet Position inside Kundali Chart
# ----------------------------
class PlanetPosition(models.Model):
    kundali = models.ForeignKey(UserKundali, on_delete=models.CASCADE, related_name="planet_positions")
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    full_degree = models.FloatField()
    norm_degree = models.FloatField()
    speed = models.FloatField()
    is_retro = models.BooleanField()
    sign = models.ForeignKey(Rashi, on_delete=models.SET_NULL, null=True)
    nakshatra = models.ForeignKey(Nakshatra, on_delete=models.SET_NULL, null=True)
    nakshatra_pad = models.IntegerField()
    house = models.ForeignKey(House, on_delete=models.SET_NULL, null=True)
    is_planet_set = models.BooleanField()
    awastha = models.ForeignKey(Awastha, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.planet.name} in {self.sign} for {self.kundali}"


# ----------------------------
# Prediction Result Model
# ----------------------------
class PredictionResult(models.Model):
    kundali = models.ForeignKey(UserKundali, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} prediction for {self.kundali}"
