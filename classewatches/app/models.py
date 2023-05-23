from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    total = models.FloatField(default=0.00, verbose_name="Total")
    billing = models.FloatField(default=0.00, verbose_name="Frete")

    def __str__(self):
        return str("Carrinho pertence ao usuário {0}, e tem um id {1}!".format(self.user.name, self.id))
    
class Order(models.Model):
    id = models.CharField(max_length=900, primary_key=True)
    

class Product(models.Model):
    id = models.AutoField(primary_key=True)

    # Many-to-many
    cart = models.ManyToManyField(Cart, editable=False, verbose_name="Carrinho")
    order = models.ManyToManyField(Order, editable=False, verbose_name="Pedido")

    title = models.CharField(max_length=25, verbose_name="Título")
    description = models.CharField(max_length=50, verbose_name="Descrição")
    price = models.FloatField(default=0.00, verbose_name="Preço")
    quantity = models.IntegerField(default=1, verbose_name="Quantidade")
    image_cover = models.FileField(upload_to='static/', verbose_name="Imagem de capa")
    image2 = models.FileField(upload_to='static/', verbose_name="Imagem 2")
    image3 = models.FileField(upload_to='static', verbose_name="Imagem 3")

    def __str__(self):
        return str("Produto {0} tem id {1}, temos {2} disponíveis. O produto custa {3}!".format(self.name, self.id, self.quantity, self.price))
