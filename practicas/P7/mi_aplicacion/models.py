# mi_aplicacion/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Libro(models.Model):
  id = models.AutoField(primary_key=True)
  titulo = models.CharField(max_length=200)
  autor  = models.CharField(max_length=100)

  def __str__(self):
    return self.titulo

  def get_libro(key, value):
    if key == 'id':
      libro = Libro.objects.all().filter(id=value)
    if key == 'titulo':
      libro = Libro.objects.all().filter(titulo=value)
    elif key == 'autor':
      libro = Libro.objects.all().filter(autor=value)
    return libro

class Prestamo(models.Model):
  id = models.AutoField(primary_key=True)
  libro   = models.ForeignKey(Libro, on_delete=models.CASCADE)
  fecha   = models.DateField(default=timezone.now)
  usuario = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.libro) + "prestado a " + str(self.usuario)

  def  get_prestamo(key, value):
    if key == 'id':
      prestamo = Prestamo.objects.all().filter(id=value)
    if key == 'libro':
      id=0
      libro = Libro.get_libro('titulo', value)
      if libro:
        id = libro[0].id
      prestamo = Prestamo.objects.all().filter(libro=id)
    elif key == 'fecha':
      prestamo = Prestamo.objects.all().filter(fecha=value)
    elif key == 'usuario':
      prestamo = Prestamo.objects.all().filter(usuario=value)
    return prestamo