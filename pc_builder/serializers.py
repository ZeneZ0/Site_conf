from rest_framework import serializers
from .models import Processor, VideoCard, Motherboard, ComputerBuild, UserFavorite

class ProcessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Processor
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class VideoCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCard
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class MotherboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motherboard
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ComputerBuildSerializer(serializers.ModelSerializer):
    processor = ProcessorSerializer(read_only=True)
    processor_id = serializers.PrimaryKeyRelatedField(
        queryset=Processor.objects.all(), source='processor', write_only=True
    )
    videocard = VideoCardSerializer(read_only=True)
    videocard_id = serializers.PrimaryKeyRelatedField(
        queryset=VideoCard.objects.all(), source='videocard', write_only=True
    )
    motherboard = MotherboardSerializer(read_only=True)
    motherboard_id = serializers.PrimaryKeyRelatedField(
        queryset=Motherboard.objects.all(), source='motherboard', write_only=True
    )

    class Meta:
        model = ComputerBuild
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class UserFavoriteSerializer(serializers.ModelSerializer):
    build = ComputerBuildSerializer(read_only=True)
    build_id = serializers.PrimaryKeyRelatedField(
        queryset=ComputerBuild.objects.all(), source='build', write_only=True
    )

    class Meta:
        model = UserFavorite
        fields = '__all__'