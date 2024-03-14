from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class City(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/cities_images', null=True, blank=True)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
    
    def __str__(self):
        return self.name


class Hotel(models.Model):
    class STARS(models.IntegerChoices):
        TWO_STARS = 2, 'دو ستاره'
        THREE_STARS = 3, 'سه ستاره'
        FOUR_STARS = 4, 'چهار ستاره'
        FIVE_STARS = 5, 'پنج ستاره'

    name = models.CharField(max_length=150)
    stars = models.PositiveSmallIntegerField(choices=STARS.choices)
    address = models.CharField(max_length=150)
    free_parking = models.BooleanField(default=False)
    free_net = models.BooleanField(default=False)
    ATM = models.BooleanField(default=True)
    elevator = models.BooleanField(default=True)
    newspaper = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    shop = models.BooleanField(default=False)
    pool = models.BooleanField(default=False)
    prayer_room = models.BooleanField(default=False)
    marriage_room = models.BooleanField(default=False)
    barbers = models.BooleanField(default=False)
    safe_box = models.BooleanField(default=False)
    lobby = models.BooleanField(default=False)
    lobby_tiolet = models.BooleanField(default=False)
    coffee_shop = models.BooleanField(default=False)
    resturant = models.BooleanField(default=True)
    breakfast_room = models.BooleanField(default=False)
    traditional_teahouse = models.BooleanField(default=False)
    conference_hall = models.BooleanField(default=False)
    green_space = models.BooleanField(default=False)
    tennis_court = models.BooleanField(default=False)
    view = models.CharField(max_length=15, null=True, blank=True)
    english_language_employees = models.BooleanField(default=False)
    lobby_sofa = models.BooleanField(default=True)
    room_service = models.BooleanField(default=False)
    laundry = models.BooleanField(default=False)
    be_awake = models.BooleanField(default=False)
    medical_services = models.BooleanField(default=False)
    shoe_wax = models.BooleanField(default=False)
    breakfast_in_room = models.BooleanField(default=False)
    lunch_in_room = models.BooleanField(default=False)
    fax = models.BooleanField(default=False)
    photocopy = models.BooleanField(default=False)
    luggage_room = models.BooleanField(default=False)
    travel_agency = models.BooleanField(default=False)
    freight_services = models.BooleanField(default=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='hotels')
    telephone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images/hotels_images', null=True, blank=True)

    @property
    def hotel_likes_count(self):
        return self.likes.count()

    def __str__(self):
        return self.name


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/hotels_images', null=True, blank=True)

    def __str__(self):
        return self.hotel.name
    
    
class Room(models.Model):
    class BREAKFAST(models.TextChoices):
        COLD = 'سرد', 'سرد'
        HOT = 'گرم', 'گرم'
        COLD_AND_HOT = 'سرد و گرم', 'سرد و گرم'

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    title = models.CharField(max_length=30)
    capacity = models.CharField(max_length=50)
    breakfast = models.CharField(max_length=30, choices=BREAKFAST.choices)
    room_number = models.IntegerField(null=True, blank=True)
    size = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField() # Price for one night
    image = models.ImageField(upload_to='images/rooms_images', null=True, blank=True)

    def __str__(self):
        return f'This room is in the {self.hotel.name} hotel'
    

class Reservation(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='reservations')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reservations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f'{self.user.phone_number} reserved {self.room.room_number} in the {self.hotel.name}'


class HotelRating(models.Model):
    RATING_CHOICES = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars')
    )
    
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name = 'ratings')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('hotel', 'user')

    def __str__(self):
        return f"{self.user}'s {self.rating}-stars rating for {self.hotel.name}"
    

class HotelComment(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='comments')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    @property
    def comment_likes_count(self):
        return self.likes.count()
    
    @property
    def comment_dislikes_count(self):
        return self.dislikes.count()
    
    """
    The following method is used in the front-end for conditions and restricting user access:
    user can not like this comment again if user liked this movie.
    user can not dislike this comment if user liked this movie.
    """
    def user_did_like(self, user):
        user_like = user.likes.filter(comment=self)
        if user_like.exists():
            return True
        return False

    def __str__(self):
        return f'{self.user} - {self.body[:10]}'
    

class CommentLike(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='comments_likes')
    comment = models.ForeignKey(HotelComment, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('comment', 'user')

    def __str__(self):
        return f'{self.user} liked {self.comment.body[:10]}'
    

class CommentDisLike(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='comments_dislikes')
    comment = models.ForeignKey(HotelComment, on_delete=models.CASCADE, related_name='dislikes')

    class Meta:
        unique_together = ('comment', 'user')
    
    def __str__(self):
        return f'{self.user} disliked {self.comment.body[:10]}'


class HotelLike(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='hotel_likes')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'hotel')
    
    def __str__(self):
        return f'{self.user} disliked {self.hotel.name}'