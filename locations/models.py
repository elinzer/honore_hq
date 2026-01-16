from django.db import models


class Unit(models.Model):
    class UnitType(models.TextChoices):
        RESIDENTIAL = 'RESIDENTIAL', 'Residential'
        COMMON = 'COMMON', 'Common Area'

    household = models.ForeignKey(
        'households.Household',
        on_delete=models.CASCADE,
        related_name='units'
    )
    name = models.CharField(max_length=100)
    unit_type = models.CharField(
        max_length=20,
        choices=UnitType.choices,
        blank=True
    )
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return f"{self.name} ({self.household})"
