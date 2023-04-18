from django.db import models
from django.utils.text import slugify
from utils import utils
from PIL import Image
from django.conf import settings

class Pizza(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    imagem = models.ImageField(upload_to='cardapio/%Y/%m', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco = models.FloatField()
    
    def get_preco_formatado(self):
        return utils.formata_preco(self.preco)
    
    get_preco_formatado.short_description = 'Preço'
    
    def resize_image(self, img, new_width = 800):
        img_path = settings.MEDIA_ROOT / img.name
        img_pil = Image.open(img_path)
        default_width, default_height = img_pil.size
        
        if default_width <= new_width:
            img_pil.close()
            return
        
        new_heigth = round((new_width * default_height) / default_width)
        new_img = img_pil.resize((new_width,new_heigth), Image.LANCZOS)
        new_img.save(img_path, optimize=True, quality=50)
        
    def save(self, *args, **kwargs):
        
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug
        
        super().save(*args, **kwargs)
        
        max_image_size = 800
        
        if self.imagem:
            self.resize_image(self.imagem, max_image_size)
            

    def __str__(self) -> str:
        return self.nome
    
class PizzaTamanhos(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    tamanho = models.CharField(max_length=255)
    preco = models.FloatField()
    
    def __str__(self):
        return self.tamanho or self.pizza.nome
    
    class Meta:
        verbose_name = 'Tamanhos de Pizza'