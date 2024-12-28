from rest_framework import serializers
from .models import CustomUser
from med.models import Medecin

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    specialite = serializers.CharField(required=False, allow_blank=True)  # Initially optional

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name', 'last_name', 'role', 'specialite']

    def validate(self, data):
        # If role is 'Médecin', check if specialite is provided
        if data.get('role') == 'Médecin' and not data.get('specialite'):
            raise serializers.ValidationError({'specialite': 'This field is required for Médecin.'})
        
        return data

    def create(self, validated_data):
        # Extract the password
        password = validated_data.pop('password')
        specialite = validated_data.pop('specialite', None)  # Get 'specialite' if available

        # Create the user
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        # Check if role is 'Médecin' and create Medecin instance
        if validated_data.get('role') == 'Médecin':
            # Create the Medecin instance, and if specialite is provided, pass it
            medecin_data = {'user': user}
            if specialite:
                medecin_data['specialite'] = specialite
            Medecin.objects.create(**medecin_data)

        return user
