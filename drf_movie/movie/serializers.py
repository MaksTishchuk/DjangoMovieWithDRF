from rest_framework import serializers

from .models import Movie, Review, Rating, Actor


class FilterReviewListSerializer(serializers.ListSerializer):
    """Чтобы выводить только отзывы-parents"""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children для вложенных комментариев"""

    def to_representation(self, value):
        serializer = ReviewSerializer(value, context=self.context)
        return serializer.data


class ActorListSerializer(serializers.ModelSerializer):
    """Список актеров/режиссеров"""

    class Meta:
        model = Actor
        fields = ('id', 'name', 'age', 'image')


class ActorDetailSerializer(serializers.ModelSerializer):
    """Детальная информация про актера/режисера"""

    class Meta:
        model = Actor
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    """Список фильмов"""

    rating_user = serializers.BooleanField()
    middle_star = serializers.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'category', 'year', 'rating_user', 'middle_star')


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзывов"""

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзывов"""

    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer  # отфильтровываем только отзывы-parents
        model = Review
        fields = ('name', 'text', 'children')


class MovieDetailSerializer(serializers.ModelSerializer):
    """Детали о фильме"""

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = ActorListSerializer(read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга к фильму"""

    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating
