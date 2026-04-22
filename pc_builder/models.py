from django.db import models
from django.contrib.auth.models import User

class Processor(models.Model):
    name = models.CharField(max_length=100)
    cores = models.IntegerField()
    frequency = models.FloatField()
    picture = models.ImageField("Изображение", null=True, blank=True, upload_to="processors")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class VideoCard(models.Model):
    name = models.CharField(max_length=100)
    memory = models.IntegerField()
    chipset = models.CharField(max_length=50)
    picture = models.ImageField("Изображение", null=True, blank=True, upload_to="videocards")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Motherboard(models.Model):
    name = models.CharField(max_length=100)
    socket = models.CharField(max_length=50)
    form_factor = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class ComputerBuild(models.Model):
    name = models.CharField(max_length=100)
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE)
    videocard = models.ForeignKey(VideoCard, on_delete=models.CASCADE)
    motherboard = models.ForeignKey(Motherboard, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class UserFavorite(models.Model):
    build = models.ForeignKey(ComputerBuild, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user_id} - {self.build.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    otp_key = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - OTP Key"