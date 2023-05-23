from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=25, verbose_name="Título")
    description = models.CharField(max_length=50, verbose_name="Descrição")
    price = models.FloatField(default=0.00, verbose_name="Preço")
    quantity = models.IntegerField(default=1, verbose_name="Quantidade")
    image_cover = models.FileField(upload_to='static/', verbose_name="Imagem de capa")
    image2 = models.FileField(upload_to='static/', verbose_name="Imagem 2")
    image3 = models.FileField(upload_to='static', verbose_name="Imagem 3")

    def __str__(self):
        return str("Produto {0} tem id {1}, temos {2} disponíveis. O produto custa {3}!".format(self.name, self.id, self.quantity, self.price))
    
