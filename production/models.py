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
    client_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Buyurtmachi nomi")
    fabric = models.CharField(max_length=255, verbose_name="Mato nomi")
    target_kg = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Rejalashtirilgan mato (kg)")
    actual_kg = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Amaldagi mato (kg)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.fabric} ({self.get_status_display()})"


# ==========================================
# BARCHA QOLGAN MODELLAR
# ==========================================

class Order(models.Model):
    date = models.DateField(verbose_name="Sana", blank=True, null=True)
    client_name = models.CharField(max_length=255, verbose_name="Buyurtmachi nomi", blank=True, null=True)
    order_name = models.CharField(max_length=255, verbose_name="Buyurtma nomi", blank=True, null=True)
    fabric_name = models.CharField(max_length=255, verbose_name="Mato nomi", blank=True, null=True)
    density_finish = models.CharField(max_length=100, verbose_name="Gr/m2 Iplik bo'yi (Finish)", blank=True, null=True)
    width_type = models.CharField(max_length=100, verbose_name="Eni (Tup/Mayli/Acik)", blank=True, null=True)
    machine_type = models.CharField(max_length=100, verbose_name="Dastgoh turi", blank=True, null=True)
    quantity_kg = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Buyurtma miqdori (kg)", blank=True, null=True)
    service_or_sale = models.CharField(max_length=100, verbose_name="Xizmat yoki Sotish", blank=True, null=True)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Xizmat/Sotish 1 kg narxi ($)", blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Buyurtma summasi ($)", blank=True, null=True)
    note = models.TextField(blank=True, null=True, verbose_name="Izoh")

    def __str__(self):
        return f"{self.order_name} - {self.client_name}"


class YarnIncome(models.Model):
    income_date = models.DateField(verbose_name="Ip kelgan sana")
    id_number = models.CharField(max_length=100, verbose_name="ID raqami")
    supplier_company = models.CharField(max_length=255, verbose_name="Ip kelgan korxona nomi")
    yarn_name = models.CharField(max_length=255, verbose_name="Ip nomi")
    yarn_lot = models.CharField(max_length=100, verbose_name="Ip loti")
    service_or_sale = models.CharField(max_length=100, verbose_name="Xizmat yoki Sotish")
    quantity_kg = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Ip miqdori (kg)")
    bag_count = models.IntegerField(verbose_name="Qop soni (dona)")
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="1 kg ip narxi ($)")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Jami ip narxi ($)")
    responsible_person = models.CharField(max_length=255, verbose_name="Ipni qabul qilib olgan mas'ul")

    def __str__(self):
        return f"{self.yarn_name} ({self.yarn_lot}) - {self.quantity_kg} kg"


class YarnIssue(models.Model):
    issue_date = models.DateField(verbose_name="Chiqim sanasi")
    id_number = models.CharField(max_length=100, verbose_name="ID raqami")
    yarn_name = models.CharField(max_length=255, verbose_name="Ip nomi")
    yarn_lot = models.CharField(max_length=100, verbose_name="Ip loti")
    quantity_kg = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Miqdori (kg)")
    bag_count = models.IntegerField(verbose_name="Qop soni (dona)")
    machine_number = models.CharField(max_length=100, verbose_name="Qaysi dastgoh")
    fabric_name = models.CharField(max_length=255, verbose_name="Mato nomi")
    client_name = models.CharField(max_length=255, verbose_name="Buyurtmachi")
    order_name = models.CharField(max_length=255, verbose_name="Buyurtma nomi")
    service_or_sale = models.CharField(max_length=100, verbose_name="Xizmat yoki Sotish")

    def __str__(self):
        return f"{self.yarn_name} -> {self.machine_number} ({self.quantity_kg} kg)"


class YarnReturn(models.Model):
    return_date = models.DateField(verbose_name="Qaytgan sanasi")
    id_number = models.CharField(max_length=100, verbose_name="ID raqami")
    yarn_name = models.CharField(max_length=255, verbose_name="Ip nomi")
    yarn_lot = models.CharField(max_length=100, verbose_name="Ip loti")
    quantity_kg = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Miqdori (kg)")
    client_name = models.CharField(max_length=255, verbose_name="Buyurtmachi")
    service_or_sale = models.CharField(max_length=100, verbose_name="Xizmat yoki Sotish")
    note = models.TextField(blank=True, null=True, verbose_name="Izoh")

    def __str__(self):
        return f"{self.yarn_name} - {self.quantity_kg} kg"


class YarnRefundToClient(models.Model):
    refund_date = models.DateField(verbose_name="Chiqim sanasi")
    id_number = models.CharField(max_length=100, verbose_name="ID raqami")
    yarn_name = models.CharField(max_length=255, verbose_name="Ip nomi")
    yarn_lot = models.CharField(max_length=100, verbose_name="Ip loti")
    quantity_kg = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Miqdori (kg)")
    bag_count = models.IntegerField(verbose_name="Qop soni")
    client_name = models.CharField(max_length=255, verbose_name="Buyurtmachi")
    service_or_sale = models.CharField(max_length=100, verbose_name="Xizmat yoki Sotish")
    note = models.TextField(blank=True, null=True, verbose_name="Izoh")

    def __str__(self):
        return f"Refund: {self.client_name} - {self.yarn_name}"


class FabricIncome(models.Model):
    income_date = models.DateField(verbose_name="Mato kirim sanasi")
    service_or_sale = models.CharField(max_length=100, verbose_name="Xizmat yoki Sotish")
    client_name = models.CharField(max_length=255, verbose_name="Buyurtmachi nomi")
    order_name = models.CharField(max_length=255, verbose_name="Buyurtma nomi")
    fabric_name = models.CharField(max_length=255, verbose_name="Mato nomi")
    density_finish = models.CharField(max_length=100, verbose_name="Gr/m2 Iplik bo'yi (Finish)")
    width_type = models.CharField(max_length=100, verbose_name="Eni (Tup/Mayli/Acik)")
    machine_type = models.CharField(max_length=100, verbose_name="Dastgoh turi")
    yarn_lot = models.CharField(max_length=100, verbose_name="Ip loti")
    quantity_kg = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Mato miqdori (kg)")
    roll_count = models.IntegerField(verbose_name="Rulon soni (dona)")
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="1 kg narxi ($)")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Jami narxi ($)")
    machine_number = models.CharField(max_length=100, verbose_name="Qaysi dastgohda to'qilgan")
    responsible_person = models.CharField(max_length=255, verbose_name="Qabul qilib olgan mas'ul xodim")

    def __str__(self):
        return f"{self.fabric_name} - {self.quantity_kg} kg"


class FabricDispatch(models.Model):
    dispatch_date = models.DateField(verbose_name="Mato chiqim sanasi")
    client_name = models.CharField(max_length=255, verbose_name="Buyurtmachi nomi")
    order_name = models.CharField(max_length=255, verbose_name="Buyurtma nomi")
    fabric_name = models.CharField(max_length=255, verbose_name="Mato nomi")
    density_finish = models.CharField(max_length=100, verbose_name="Gr/m2 Iplik bo'yi (Finish)")
    width_type = models.CharField(max_length=100, verbose_name="Eni (Tup/Mayli/Acik)")
    machine_type = models.CharField(max_length=100, verbose_name="Dastgoh turi")
    yarn_lot = models.CharField(max_length=100, verbose_name="Ip loti")
    quantity_kg = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Mato miqdori (kg)")
    roll_count = models.IntegerField(verbose_name="Rulon soni (dona)")
    machine_number = models.CharField(max_length=100, verbose_name="Qaysi dastgohda to'qilgan")
    service_or_sale = models.CharField(max_length=100, verbose_name="Xizmat yoki Sotish")
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="1 kg narxi ($)")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Jami narxi ($)")

    def __str__(self):
        return f"Dispatch: {self.client_name} - {self.fabric_name}"