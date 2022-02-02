from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio',
                  'role']


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio',
                  'role']
        read_only_fields = ['role']


class SignUpSerializer(serializers.ModelSerializer):
    BANED_USERNAMES = ['me']

    class Meta:
        model = User
        fields = ['username', 'email']

    def validate_username(self, value):
        if value in self.BANED_USERNAMES:
            raise serializers.ValidationError(
                {
                    'username': f'Использовать имя "{value}" запрещено.'
                }
            )

        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    def validate(self, data):
        user = get_object_or_404(User, username=data.get('username'))

        token_valid = default_token_generator.check_token(
            user, data.get('confirmation_code')
        )

        if not token_valid:
            raise serializers.ValidationError(
                {
                    'confirmation_code': 'Token is invalid or expired. Please '
                                         'request another confirmation email '
                                         'by signing in.'
                }
            )

        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, attrs):
        if self.context['request']._request.method != 'POST':
            return attrs

        if Review.objects.filter(
                title_id=self.context['view'].kwargs['title_id'],
                author=self.context['request'].user
        ).exists():
            raise serializers.ValidationError(
                'Вы уже писали отзыв на это произведение.'
            )
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug', )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug', )


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        read_only=True
    )
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=False
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        required=False, many=True
    )

    class Meta:
        model = Title
        fields = '__all__'
