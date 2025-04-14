from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from import_export.admin import ImportExportModelAdmin
from .models import (
    Planet, Rashi, Nakshatra, Element, Awastha, House,
    UserKundali, PlanetPosition, PredictionResult,
    Language, Alias
)

# ----------------------------
# Inline for Aliases
# ----------------------------
class AliasInline(GenericTabularInline):
    model = Alias
    extra = 1
    autocomplete_fields = ['language']

# ----------------------------
# Language Admin
# ----------------------------
@admin.register(Language)
class LanguageAdmin(ImportExportModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']

# ----------------------------
# Alias Admin
# ----------------------------
@admin.register(Alias)
class AliasAdmin(ImportExportModelAdmin):
    list_display = ['name', 'language', 'content_type', 'object_id']
    search_fields = ['name']
    list_filter = ['language', 'content_type']

# ----------------------------
# Planet Admin
# ----------------------------
@admin.register(Planet)
class PlanetAdmin(ImportExportModelAdmin):
    list_display = ['name', 'is_visible', 'is_shadow', 'is_lagna']
    search_fields = ['name']
    list_filter = ['is_visible', 'is_shadow', 'is_malefic']
    inlines = [AliasInline]

# ----------------------------
# Rashi Admin
# ----------------------------
@admin.register(Rashi)
class RashiAdmin(ImportExportModelAdmin):
    list_display = ['name', 'lord', 'element']
    search_fields = ['name', 'lord__name']
    autocomplete_fields = ['lord', 'element']
    list_filter = ['element']
    inlines = [AliasInline]

# ----------------------------
# Nakshatra Admin
# ----------------------------
@admin.register(Nakshatra)
class NakshatraAdmin(ImportExportModelAdmin):
    list_display = ['name', 'lord']
    search_fields = ['name', 'lord__name']
    inlines = [AliasInline]

# ----------------------------
# Element Admin
# ----------------------------
@admin.register(Element)
class ElementAdmin(ImportExportModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    inlines = [AliasInline]

# ----------------------------
# Awastha Admin
# ----------------------------
@admin.register(Awastha)
class AwasthaAdmin(ImportExportModelAdmin):
    list_display = ['name']
    search_fields = ['name']

# ----------------------------
# House Admin
# ----------------------------
@admin.register(House)
class HouseAdmin(ImportExportModelAdmin):
    list_display = ['number']

# ----------------------------
# PlanetPosition Inline for UserKundali
# ----------------------------
class PlanetPositionInline(admin.TabularInline):
    model = PlanetPosition
    extra = 1

# ----------------------------
# UserKundali Admin
# ----------------------------
@admin.register(UserKundali)
class UserKundaliAdmin(ImportExportModelAdmin):
    list_display = ['user', 'chart_type', 'ascendant', 'created_at']
    list_filter = ['chart_type', 'created_at']
    search_fields = ['user__username']
    inlines = [PlanetPositionInline]

# ----------------------------
# PlanetPosition Admin
# ----------------------------
@admin.register(PlanetPosition)
class PlanetPositionAdmin(ImportExportModelAdmin):
    list_display = ['kundali', 'planet', 'sign', 'house', 'is_retro']
    list_filter = ['planet', 'sign', 'house', 'is_retro']
    search_fields = ['kundali__user__username']

# ----------------------------
# PredictionResult Admin
# ----------------------------
@admin.register(PredictionResult)
class PredictionResultAdmin(ImportExportModelAdmin):
    list_display = ['kundali', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['kundali__user__username', 'category']
