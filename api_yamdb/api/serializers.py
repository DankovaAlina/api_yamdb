from rest_framework import serializers

from reviews.models import User


class UserFullInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value


class UserSignupSerializer(UserFullInfoSerializer):

    class Meta(UserFullInfoSerializer.Meta):
        fields = ('email', 'username')


class UserTokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField()
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserInfoForUserSerializer(UserFullInfoSerializer):

    class Meta(UserFullInfoSerializer.Meta):
        read_only_fields = ('role',)
