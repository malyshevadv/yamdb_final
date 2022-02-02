from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserLoadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio',
                  'role']


class ReviewLoadSerializer(serializers.ModelSerializer):
    title_id = serializers.PrimaryKeyRelatedField(queryset=Title.objects.all(),
                                                  source='title')

    class Meta:
        model = Review
        fields = ['title_id', 'text', 'author', 'score', 'pub_date']


class GenreLoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']


class CategoryLoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class TitleLoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ['name', 'year', 'category']


class TitleGenresLoadSerializer(serializers.Serializer):
    title_id = serializers.IntegerField()
    genre_id = serializers.IntegerField()

    def save(self):
        title = Title.objects.get(id=self.validated_data['title_id'])
        genre = Genre.objects.get(id=self.validated_data['genre_id'])
        title.genre.add(genre)


class CommentLoadSerializer(serializers.ModelSerializer):
    review_id = serializers.PrimaryKeyRelatedField(
        queryset=Review.objects.all(),
        source='review'
    )

    class Meta:
        model = Comment
        fields = ['review_id', 'text', 'author', 'pub_date']
