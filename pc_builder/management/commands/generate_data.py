from django.core.management.base import BaseCommand
from faker import Faker
from pc_builder.models import Processor, VideoCard, Motherboard, ComputerBuild, UserFavorite
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        
        users = list(User.objects.all())
        if not users:
            user = User.objects.create_user(username='testuser', password='123456')
            users = [user]
        
        self.stdout.write('Генерация процессоров...')
        processors = []
        for _ in range(200):
            processor = Processor.objects.create(
                name=fake.random_element(elements=['Intel Core i3', 'Intel Core i5', 'Intel Core i7', 'Intel Core i9', 'AMD Ryzen 3', 'AMD Ryzen 5', 'AMD Ryzen 7', 'AMD Ryzen 9']) + ' ' + fake.bothify(text='####'),
                cores=fake.random_int(min=2, max=16),
                frequency=fake.random_int(min=2000, max=5000) / 1000,
                user=fake.random_element(elements=users)
            )
            processors.append(processor)
        
        self.stdout.write('Генерация видеокарт...')
        videocards = []
        for _ in range(200):
            videocard = VideoCard.objects.create(
                name=fake.random_element(elements=['NVIDIA GeForce RTX', 'AMD Radeon RX']) + ' ' + fake.bothify(text='####'),
                memory=fake.random_int(min=4, max=24),
                chipset=fake.random_element(elements=['NVIDIA', 'AMD', 'Intel']),
                user=fake.random_element(elements=users)
            )
            videocards.append(videocard)
        
        self.stdout.write('Генерация материнских плат...')
        motherboards = []
        for _ in range(200):
            motherboard = Motherboard.objects.create(
                name=fake.random_element(elements=['ASUS', 'MSI', 'Gigabyte', 'ASRock']) + ' ' + fake.bothify(text='???-####'),
                socket=fake.random_element(elements=['LGA1700', 'LGA1200', 'AM5', 'AM4']),
                form_factor=fake.random_element(elements=['ATX', 'Micro-ATX', 'Mini-ITX']),
                user=fake.random_element(elements=users)
            )
            motherboards.append(motherboard)
        
        self.stdout.write('Генерация сборок ПК...')
        builds = []
        for _ in range(400):
            build = ComputerBuild.objects.create(
                name=fake.random_element(elements=['Игровой', 'Офисный', 'Рабочий', 'Для стриминга', 'Бюджетный']) + ' ПК ' + fake.bothify(text='##'),
                processor=fake.random_element(elements=processors),
                videocard=fake.random_element(elements=videocards),
                motherboard=fake.random_element(elements=motherboards),
                price=fake.random_int(min=30000, max=300000),
                user=fake.random_element(elements=users)
            )
            builds.append(build)
        
        self.stdout.write('Генерация избранного...')
        for _ in range(200):
            UserFavorite.objects.create(
                build=fake.random_element(elements=builds),
                user_id=fake.random_element(elements=users).id
            )
        
        self.stdout.write(f'Процессоров: {Processor.objects.count()}')
        self.stdout.write(f'Видеокарт: {VideoCard.objects.count()}')
        self.stdout.write(f'Материнских плат: {Motherboard.objects.count()}')
        self.stdout.write(f'Сборок ПК: {ComputerBuild.objects.count()}')
        self.stdout.write(f'Избранного: {UserFavorite.objects.count()}')