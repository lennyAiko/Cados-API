from rest_framework.serializers import ModelSerializer
from .models import Advocate, Company

class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class AdvocateSerializer(ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Advocate
        fields = [
            'username', 'bio', 'company'
        ]

