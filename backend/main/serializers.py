import json
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.gis.geos import GEOSGeometry

from .models import *#AttributeDataT, GeoJSONFile, Project, RasterFile, SpatialDataT, Vector


class VectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vector
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # model = get_user_model()
        # fields = ('username', 'email',)
        # fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_picture']
        # read_only_fields = ()


class resetpasswordSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = '__all__'

    def save(self):
        username = self.validated_data['username']
        password = self.validated_data['password']
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError(
                {'error': 'please enter valid crendentials'}
            )


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

#     def __init__(self, *args, **kwargs):
#         include_password2 = kwargs.pop('include_password2', False)

#         if include_password2:
#             self.Meta.fields += ['password2']
#         print("B"*50)
#         super().__init__(*args, **kwargs)

#     def validate(self, data):
#         if "password2" in data.keys():
#             if data['password'] != data['password2']:
#                 raise serializers.ValidationError("Passwords do not match")
#         print("A"*50)
#         return data

#     def create(self, validated_data):
#         validated_data.pop('password2', None)
#         return super().create(validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data


class GeoJsonFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoJSONFile
        fields = ('id', 'name', 'geojson', 'attributes')


class RasterFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RasterFile
        fields = ('id', 'name', 'user', 'raster',"tiles","png")
        # fields = ('id', 'name', 'user', 'raster')

        validators = [
            FileExtensionValidator(allowed_extensions=['tif', 'tiff']),
            validate_file_size
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.method == 'GET':
            # if instance.png.name!='':
            #     data['png'] = instance.png
            if instance.tiles != '':
                data['tiles'] = instance.tiles

        return data


class ProjectSerializer(serializers.ModelSerializer):

    vector = VectorSerializer(many=True, read_only=True)
    raster = RasterFileSerializer(many=True, read_only=True)
    geojson = GeoJsonFileSerializer(many=True, read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_created_at(self, obj):
        return obj.get_create_at()

    def get_updated_at(self, obj):
        return obj.get_updated_at()
    
    def create(self, validated_data):
        name = validated_data['name']
        user = validated_data['user']

        project = Project.objects.create(name=name, user=user)
        return project


class UserRegister(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'], email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SpatialDataSerializer(serializers.ModelSerializer):
    geom = serializers.JSONField()  # Use JSONField para a geometria

    class Meta:
        model = SpatialDataT
        fields = '__all__'

    def create(self, validated_data):
        # Converta a geometria JSON em um objeto de geometria
        geom_json = validated_data.pop('geom')
        geom_str = json.dumps(geom_json)
        geom = GEOSGeometry(geom_str)
        
        spatial_data = SpatialDataT(geom=geom, **validated_data)
        spatial_data.save()
        return spatial_data

# class AttributesDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AttributeDataT
#         fields = '__all__'
        