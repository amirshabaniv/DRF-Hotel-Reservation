from django.contrib import admin
from .models import City, Hotel, HotelImage, Room, Reservation, HotelRating, HotelComment, CommentLike, CommentDisLike


class HotelImagesInline(admin.TabularInline):
    model = HotelImage

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelImagesInline]
    raw_id_fields = ('city',)

admin.site.register(City)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    raw_id_fields = ('hotel',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'hotel', 'room')

@admin.register(HotelRating)
class HotelRatingAdmin(admin.ModelAdmin):
    raw_id_fields = ('hotel', 'user')

@admin.register(HotelComment)
class HotelCommentAdmin(admin.ModelAdmin):
    raw_id_fields = ('hotel', 'user')

@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'comment')

@admin.register(CommentDisLike)
class CommentDisLikeAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'comment')