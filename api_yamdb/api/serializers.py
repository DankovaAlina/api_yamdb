from rest_framework import serializers

from reviews.models import User, Category, Genre, Title


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
     
    
class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категории.
    """

    class Meta:
        model = Category
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор заголовка.
    """

    category = CategorySerializer()
    genre = serializers.StringRelatedField()

    class Meta:
        model = Title
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанра.
    """

    class Meta:
        model = Genre
        fields = '__all__'
