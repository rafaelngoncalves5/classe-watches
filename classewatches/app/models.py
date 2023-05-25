from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    total = models.FloatField(default=0.00, verbose_name="Total")
    billing = models.FloatField(default=0.00, verbose_name="Frete")

    def __str__(self):
        return str("Carrinho pertence ao usuário {0}, e tem um id {1}!".format(self.user.username, self.id))
    
class Order(models.Model):
     
    STATUS_ENUM = [
        ('pendente', 'pendente'),
        ('aceito', 'aceito'),
        ('despachado', 'despachado')
    ]
    
    id = models.CharField(max_length=900, primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Carrinho")
    total = models.FloatField(default=0.00, verbose_name="Total")
    order_date = models.DateField(default=timezone.now, auto_now_add=False, verbose_name="Data do pedido")
    phone_number = models.CharField(max_length=14, verbose_name="Telefone")
    phone_number2 = models.CharField(max_length=14, verbose_name="Telefone 2")
    state = models.CharField(max_length=25, verbose_name="Estado")
    district = models.CharField(max_length=25, verbose_name="Bairro")
    street = models.CharField(max_length=25, verbose_name="Rua")
    street_number = models.IntegerField(verbose_name="Número da rua")
    complement = models.CharField(max_length=150, null=True, verbose_name="Complemento")
    cep = models.CharField(verbose_name="CEP", max_length=150)
    status = models.CharField(choices=STATUS_ENUM, verbose_name="Status", default=STATUS_ENUM[0][1], max_length=25)
    tracking_link = models.URLField(verbose_name="Link de rastreamento", null=True)

    def __str__(self):
        return str(f"Pedido com id {self.id}, do carrinho {self.cart.id}, num valor total de R$ {self.total}!")

class Product(models.Model):
    id = models.AutoField(primary_key=True)

    # Many-to-many
    cart = models.ManyToManyField(Cart, editable=False, verbose_name="Carrinho")
    order = models.ManyToManyField(Order, editable=False, verbose_name="Pedido")

    title = models.CharField(max_length=25, verbose_name="Título")
    description = models.CharField(max_length=150, verbose_name="Descrição")
    price = models.FloatField(default=0.00, verbose_name="Preço")
    quantity = models.IntegerField(default=1, verbose_name="Quantidade")

    # Images
    image_cover = models.FileField(upload_to='static/', verbose_name="Imagem de capa")
    image2 = models.FileField(upload_to='static/', verbose_name="Imagem 2")
    image3 = models.FileField(upload_to='static', verbose_name="Imagem 3")

    def __str__(self):
        return str("Produto {0} tem id {1}, temos {2} unidade(s) em estoque. O produto custa R$ {3}!".format(self.title, self.id, self.quantity, self.price))
