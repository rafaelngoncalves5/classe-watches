from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    total = models.FloatField(default=0.00, verbose_name="Total")
    shipping = models.FloatField(default=0.00, verbose_name="Frete")

    def __str__(self):
        return str("Carrinho pertence ao usuário {0}, e tem um id {1}!".format(self.user.username, self.id))

class Product(models.Model):
    id = models.AutoField(primary_key=True)

    # Many-to-many
    cart = models.ManyToManyField(Cart, editable=False, verbose_name="Carrinho")

    title = models.CharField(max_length=25, verbose_name="Título")
    description = models.CharField(max_length=150, verbose_name="Descrição")
    price = models.FloatField(default=0.00, verbose_name="Preço")
    quantity = models.IntegerField(default=1, verbose_name="Quantidade")

    # Images
    image_cover = models.FileField(upload_to='static/', verbose_name="Imagem de capa", help_text="Por favor, tire a foto na vertical.")
    image2 = models.FileField(upload_to='static/', verbose_name="Imagem 2", help_text="Por favor, tire a foto na vertical.")
    image3 = models.FileField(upload_to='static', verbose_name="Imagem 3", help_text="Por favor, tire a foto na vertical.")

    def __str__(self):
        return str("Produto {0} tem id {1}, temos {2} unidade(s) em estoque. O produto custa R$ {3}!".format(self.title, self.id, self.quantity, self.price))


class Order(models.Model):
     
    STATUS_ENUM = [
        ('pendente', 'pendente'),
        ('aceito', 'aceito'),
        ('despachado', 'despachado')
    ]
    
    id = models.SlugField(max_length=900, primary_key=True, null=False)
    first_name = models.CharField(null=False, max_length=150, verbose_name='Primeiro nome')
    last_name = models.CharField(null=False, max_length=150, verbose_name='Sobrenome')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Carrinho")
    products = models.ManyToManyField(Product, verbose_name="Produtos")
    total = models.FloatField(default=0.00, verbose_name="Total")
    order_date = models.DateField(default=timezone.now, auto_now_add=False, verbose_name="Data do pedido")
    phone_number = models.CharField(max_length=14, verbose_name="Telefone")
    phone_number2 = models.CharField(max_length=14, verbose_name="Telefone 2")
    state = models.CharField(max_length=25, verbose_name="Estado")
    city = models.CharField(max_length=50, verbose_name='Cidade')
    apartment = models.CharField(null=True, default='S/N', verbose_name="Número da residência", help_text="Anule, se não tiver")
    floor = models.CharField(null=True, help_text="Anule, se não tiver", default='S/N', max_length=6, verbose_name="Andar", )
    district = models.CharField(max_length=25, verbose_name="Bairro")
    street = models.CharField(max_length=25, verbose_name="Rua")
    street_number = models.IntegerField(verbose_name="Número da rua")
    complement = models.CharField(max_length=150, null=True, verbose_name="Complemento")
    postal_code = models.CharField(verbose_name="CEP", max_length=150)
    status = models.CharField(choices=STATUS_ENUM, verbose_name="Status", default=STATUS_ENUM[0][1], max_length=25)
    tracking_link = models.URLField(verbose_name="Link de rastreamento", null=True, default="Não despachado")

    def __str__(self):
        return str(f"Pedido de {self.cart.user.username}, em {self.order_date.day}/{self.order_date.month}/{self.order_date.year}")
