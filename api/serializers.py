from rest_framework import serializers

from api.models import Project, Excel, District, Municipality, Province
from api.municipality import municipality_detail


class ProjectSerializer(serializers.ModelSerializer):
    # district = serializers.StringRelatedField()
    # municipality = serializers.StringRelatedField()
    # province = serializers.StringRelatedField()

    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    municipality = serializers.PrimaryKeyRelatedField(queryset=Municipality.objects.all())
    province = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all())
    
    # district = serializers.CharField(source='district.name')
    # municipality = serializers.CharField(source='municipality.name')
    # province = serializers.CharField(source='province.name')

    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, instance):
        project =  super().to_representation(instance)
        request = self.context.get('request')
        if request and request.method == 'GET':
            project['district'] = instance.district.name
            project['municipality'] = instance.municipality.name
            project['province'] = instance.province.name
        return project


class ExcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excel
        fields = '__all__'
    

class SummarySerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 200)
    project_count = serializers.IntegerField()
    budget = serializers.DecimalField(decimal_places=2, max_digits=15)

class SecondSummarySerializer(serializers.Serializer):
    # id  = serializers.IntegerField()
    name = serializers.CharField(max_length = 200)
    count = serializers.IntegerField()
    budget = serializers.DecimalField(decimal_places= 2, max_digits=15)

class ProvinceSerializer(serializers.ModelSerializer):
    districts = serializers.StringRelatedField(read_only = True, many = True)

    class Meta:
        model = Province
        fields = '__all__'
        fields = ['id', 'code','name','districts']
        # fields += 'districts'
        
        

class DistrictSerializer(serializers.ModelSerializer):
    municipalities = serializers.StringRelatedField(read_only = True, many = True)
    class Meta:
        model = District
        fields = '__all__'


class MunicipalitySerializer(serializers.ModelSerializer):
    district = serializers.StringRelatedField()
    province = serializers.StringRelatedField()
    class Meta:
        model = Municipality
        fields = '__all__'

