from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import AnimalType, Breed, Animal, Weighting

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)

    actions = ['toggle_user_status']

    def toggle_user_status(self, request, queryset):
        for user in queryset:
            user.toggle_active()

    toggle_user_status.short_description = "Включить/выключить пользователей"


class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'inventory_number', 'breed', 'gender', 'arrival_date', 'age_at_arrival', 'parent')
    list_filter = ('breed', 'gender', 'arrival_date')
    search_fields = ('name', 'inventory_number')
    ordering = ('arrival_date',)


class WeightingAdmin(admin.ModelAdmin):
    list_display = ('animal', 'date', 'weight', 'user')
    list_filter = ('animal', 'date')
    search_fields = ('animal__name',)
    ordering = ('date',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            return queryset.filter(user=request.user)
        return queryset

    def has_change_permission(self, request, obj=None):
        if obj and obj.user != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj and obj.user != request.user:
            return False
        return True


class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'animal_type')
    list_filter = ('animal_type',)


admin.site.register(AnimalType)
admin.site.register(Breed, BreedAdmin)
admin.site.register(Animal, AnimalAdmin)
admin.site.register(Weighting, WeightingAdmin)
admin.site.register(User, UserAdmin)