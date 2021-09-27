from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        # kwargs = Key Word Arguments

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)
        # The 'validated_data' would be the information that was passed to our
        # program via a JSON or XML file. The ** 'unwinds' that data to use


class AuthTokenSerializer(serializers.Serializer):
    """Serializaer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        """Validate the attributes of this class. Which should be what
            we defined above"""
        email = attrs.get('email')  # These attrs come in key-value pairs
        password = attrs.get('password')
        print("\nAuthTokenSerializer Class: Priting Attributes")
        print(attrs)

        """The Django REST framework has html properties. This is why the
        arguments here are 'reqeust = info' """
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:  # authentication failed
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
            """This serializers.ValidationError will be handled by the
            Django rest framework where it'll send a 400 Messages with
            the message you wish to send"""

        attrs['user'] = user
        return attrs
