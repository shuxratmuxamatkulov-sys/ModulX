from django.db import models

class Yarn(models.Model):
    """Ip zaxiralari"""
    name = models.CharField(max_length=100)  # Masalan: 30/1 Xlopok
    title_num = models.CharField(max_length=50, blank=True, null=True)  # Ne / Nm
    quantity_kg = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    supplier = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.quantity_kg} kg)"

class Fabric(models.Model):
    """Mato zaxiralari"""
    name = models.CharField(max_length=100)  # Masalan: Suprim, Kupon, Interlok
    color = models.CharField(max_length=50, blank=True, null=True)
    density = models.IntegerField(help_text="Plotnost (g/m2)", null=True, blank=True)
    quantity_kg = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    quantity_rolls = models.IntegerField(default=0, help_text="Rulonlar soni")

    def __str__(self):
        return f"{self.name} - {self.color} ({self.quantity_kg} kg)"