from django.db import models
from inventory.models import Yarn, Fabric

class ProductionRecipe(models.Model):
    """Mato to'qish resepti (BOM - Bill of Materials)"""
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE, related_name='recipes', verbose_name="Chiqadigan mato")
    yarn = models.ForeignKey(Yarn, on_delete=models.CASCADE, related_name='used_in_recipes', verbose_name="Ishlatiladigan ip")
    percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Ip nisbati (%)", default=100)

    def __str__(self):
        return f"{self.fabric.name} -> {self.yarn.name} ({self.percentage}%)"

class ProductionOrder(models.Model):
    """Ishlab chiqarish buyurtmasi / Sech topshirig'i"""
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('in_progress', 'Jarayonda'),
        ('completed', 'Tugallandi'),
        ('cancelled', 'Bekor qilindi'),
    )
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE)
    target_kg = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Rejalashtirilgan mato (kg)")
    actual_kg = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Amaldagi mato (kg)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.fabric.name} ({self.get_status_display()})"