import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from pc_builder.models import Processor, VideoCard, Motherboard, ComputerBuild, UserFavorite

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def processor():
    return baker.make(Processor)

@pytest.fixture
def videocard():
    return baker.make(VideoCard)

@pytest.fixture
def motherboard():
    return baker.make(Motherboard)

@pytest.fixture
def computer_build(processor, videocard, motherboard):
    return baker.make(ComputerBuild, processor=processor, videocard=videocard, motherboard=motherboard)

@pytest.fixture
def user_favorite(computer_build):
    return baker.make(UserFavorite, build=computer_build)


# ========== TESTS FOR PROCESSOR ==========

@pytest.mark.django_db
class TestProcessorViewSet:
    def test_list_processors(self, api_client):
        baker.make(Processor, _quantity=3)
        response = api_client.get('/api/processors/')
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_create_processor(self, api_client):
        data = {'name': 'Intel i7', 'cores': 8, 'frequency': 3.6}
        response = api_client.post('/api/processors/', data)
        assert response.status_code == 201
        assert Processor.objects.count() == 1
        assert Processor.objects.first().name == 'Intel i7'

    def test_update_processor(self, api_client, processor):
        data = {'name': 'AMD Ryzen 5', 'cores': 6, 'frequency': 4.0}
        response = api_client.patch(f'/api/processors/{processor.id}/', data)
        processor.refresh_from_db()
        assert response.status_code == 200
        assert processor.name == 'AMD Ryzen 5'

    def test_delete_processor(self, api_client, processor):
        response = api_client.delete(f'/api/processors/{processor.id}/')
        assert response.status_code == 204
        assert Processor.objects.count() == 0


# ========== TESTS FOR VIDEOCARD ==========

@pytest.mark.django_db
class TestVideoCardViewSet:
    def test_list_videocards(self, api_client):
        baker.make(VideoCard, _quantity=3)
        response = api_client.get('/api/videocards/')
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_create_videocard(self, api_client):
        data = {'name': 'RTX 3060', 'memory': 12, 'chipset': 'NVIDIA'}
        response = api_client.post('/api/videocards/', data)
        assert response.status_code == 201
        assert VideoCard.objects.count() == 1
        assert VideoCard.objects.first().name == 'RTX 3060'

    def test_update_videocard(self, api_client, videocard):
        data = {'name': 'RX 6700 XT', 'memory': 12, 'chipset': 'AMD'}
        response = api_client.patch(f'/api/videocards/{videocard.id}/', data)
        videocard.refresh_from_db()
        assert response.status_code == 200
        assert videocard.name == 'RX 6700 XT'

    def test_delete_videocard(self, api_client, videocard):
        response = api_client.delete(f'/api/videocards/{videocard.id}/')
        assert response.status_code == 204
        assert VideoCard.objects.count() == 0


# ========== TESTS FOR MOTHERBOARD ==========

@pytest.mark.django_db
class TestMotherboardViewSet:
    def test_list_motherboards(self, api_client):
        baker.make(Motherboard, _quantity=3)
        response = api_client.get('/api/motherboards/')
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_create_motherboard(self, api_client):
        data = {'name': 'B450 Tomahawk', 'socket': 'AM4', 'form_factor': 'ATX'}
        response = api_client.post('/api/motherboards/', data)
        assert response.status_code == 201
        assert Motherboard.objects.count() == 1
        assert Motherboard.objects.first().name == 'B450 Tomahawk'

    def test_update_motherboard(self, api_client, motherboard):
        data = {'name': 'Z690 Aorus', 'socket': 'LGA1700', 'form_factor': 'ATX'}
        response = api_client.patch(f'/api/motherboards/{motherboard.id}/', data)
        motherboard.refresh_from_db()
        assert response.status_code == 200
        assert motherboard.name == 'Z690 Aorus'

    def test_delete_motherboard(self, api_client, motherboard):
        response = api_client.delete(f'/api/motherboards/{motherboard.id}/')
        assert response.status_code == 204
        assert Motherboard.objects.count() == 0


# ========== TESTS FOR COMPUTERBUILD ==========

@pytest.mark.django_db
class TestComputerBuildViewSet:
    def test_list_builds(self, api_client, processor, videocard, motherboard):
        baker.make(ComputerBuild, processor=processor, videocard=videocard, motherboard=motherboard, _quantity=3)
        response = api_client.get('/api/builds/')
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_create_build(self, api_client, processor, videocard, motherboard):
        data = {
            'name': 'Gaming PC',
            'processor_id': processor.id,
            'videocard_id': videocard.id,
            'motherboard_id': motherboard.id,
            'price': 1500.00
        }
        response = api_client.post('/api/builds/', data)
        assert response.status_code == 201
        assert ComputerBuild.objects.count() == 1
        assert ComputerBuild.objects.first().name == 'Gaming PC'

    def test_update_build(self, api_client, computer_build):
        data = {'name': 'Workstation PC', 'price': 2000.00}
        response = api_client.patch(f'/api/builds/{computer_build.id}/', data)
        computer_build.refresh_from_db()
        assert response.status_code == 200
        assert computer_build.name == 'Workstation PC'
        assert computer_build.price == 2000.00

    def test_delete_build(self, api_client, computer_build):
        response = api_client.delete(f'/api/builds/{computer_build.id}/')
        assert response.status_code == 204
        assert ComputerBuild.objects.count() == 0


# ========== TESTS FOR USERFAVORITE ==========

@pytest.mark.django_db
class TestUserFavoriteViewSet:
    def test_list_favorites(self, api_client, user_favorite):
        response = api_client.get('/api/favorites/')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_create_favorite(self, api_client, computer_build):
        data = {'build_id': computer_build.id, 'user_id': 1}
        response = api_client.post('/api/favorites/', data)
        assert response.status_code == 201
        assert UserFavorite.objects.count() == 1
        assert UserFavorite.objects.first().user_id == 1

    def test_update_favorite(self, api_client, user_favorite):
        data = {'user_id': 999}
        response = api_client.patch(f'/api/favorites/{user_favorite.id}/', data)
        user_favorite.refresh_from_db()
        assert response.status_code == 200
        assert user_favorite.user_id == 999

    def test_delete_favorite(self, api_client, user_favorite):
        response = api_client.delete(f'/api/favorites/{user_favorite.id}/')
        assert response.status_code == 204
        assert UserFavorite.objects.count() == 0