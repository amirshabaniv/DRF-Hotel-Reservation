from .models import City, Hotel, HotelImage, Room, HotelRating, Reservation, HotelComment, HotelLike, CommentLike, CommentDisLike

from rest_framework import serializers

from statistics import mean
from datetime import datetime


class CitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = City
        fields = ['id', 'name', 'image']


class HotelRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelRating
        fields = ["id", "rating", "description"]
    
    def create(self, validated_data):
        cinema_id = self.context["cinema_id"]
        user_id = self.context["user_id"]
        rating = HotelRating.objects.create(cinema_id = cinema_id, user_id=user_id, **self.validated_data)
        return rating


class HotelCommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = HotelComment
        fields = ['id', 'user', 'hotel', 'content',
                  'created', 'comment_likes_count',
                  'comment_dislikes_count']


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['id', 'hotel', 'title', 'capacity', 'breakfast',
                  'room_number', 'size', 'description', 'price', 'image']
    

class HotelImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelImage
        fields = ['id', 'hotel', 'image']


class RoomForHotelSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    num_nights = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'image', 'capacity', 'breakfast', 'price', 'num_nights', 'total_price']

    def get_num_nights(self, obj):
        check_in = self.context['request'].query_params.get('check_in')
        check_out = self.context['request'].query_params.get('check_out')
        if check_in and check_out:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            num_nights = (check_out_date - check_in_date).days
            return num_nights
        return 1     
    
    def get_total_price(self, room):
        check_in = self.context['request'].query_params.get('check_in')
        check_out = self.context['request'].query_params.get('check_out')

        if check_in and check_out:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            num_nights = (check_out_date - check_in_date).days
            total_price = room.price * num_nights
            return total_price

        return None


class HotelSerializer(serializers.ModelSerializer):
    ratings_avg = serializers.SerializerMethodField(method_name='avg_ratings')
    images = HotelImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only=True)
    rooms = RoomForHotelSerializer(many=True)
    comments = HotelCommentSerializer(many=True)
    min_room_price = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'stars', 'address', 'free_parking',
                  'free_net', 'ATM', 'elevator', 'newspaper', 'gym',
                  'shop', 'pool', 'prayer_room', 'marriage_room',
                  'barbers', 'safe_box', 'lobby', 'lobby_tiolet',
                  'coffee_shop', 'resturant', 'breakfast_room',
                  'traditional_teahouse', 'conference_hall',
                  'green_space', 'tennis_court', 'view', 'english_language_employees',
                  'lobby_sofa', 'room_service', 'laundry', 'be_awake', 'medical_services',
                  'shoe_wax', 'breakfast_in_room', 'lunch_in_room', 'fax', 'photocopy',
                  'luggage_room', 'travel_agency', 'freight_services', 'city', 'image', 'telephone_number',
                  'hotel_likes_count', 'ratings_avg', 'images', 'uploaded_images', 'rooms', 'comments', 'min_room_price']
    
    def get_min_room_price(self, hotel):
        min_room_price = None
        for room in hotel.rooms.all():
            if (min_room_price is None) or (room.price < min_room_price):
                min_room_price = room.price
                return min_room_price

    def avg_ratings(self, hotel:Hotel):
        hotel_ratings = hotel.ratings.all()
        if hotel_ratings.exists():
            avg = mean([item.rating for item in hotel_ratings])
            return avg
        return 0
    

class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'hotel', 'room',
                  'check_in', 'check_out']
        

class CommentLikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'comment']


class CommentDisLikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CommentDisLike
        fields = ['id', 'user', 'comment']

        
class HotelLikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = HotelLike
        fields = ['id', 'hotel', 'user']


class HotelHomeSerializer(serializers.ModelSerializer):
    min_room_price = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'stars', 'min_room_price']

    def get_min_room_price(self, hotel):
        min_room_price = None
        for room in hotel.rooms.all():
            if (min_room_price is None) or (room.price < min_room_price):
                min_room_price = room.price
                return min_room_price


class PopularHotelSerializer(serializers.ModelSerializer):
    ratings_avg = serializers.SerializerMethodField(method_name='avg_ratings')
    min_room_price = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'stars', 'address', 'ratings_avg', 'min_room_price']

    def avg_ratings(self, hotel:Hotel):
        hotel_ratings = hotel.ratings.all()
        if hotel_ratings.exists():
            avg = mean([item.rating for item in hotel_ratings])
            return avg
        return 0
    
    def get_min_room_price(self, hotel):
        min_room_price = None
        for room in hotel.rooms.all():
            if (min_room_price is None) or (room.price < min_room_price):
                min_room_price = room.price
                return min_room_price
            