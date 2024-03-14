from .models import Hotel, HotelLike, HotelComment, CommentLike, CommentDisLike, Room
from .serializers import HotelSerializer, HotelCommentSerializer, RoomSerializer, HotelHomeSerializer, PopularHotelSerializer
from .serializers import HotelLikeSerializer, CommentLikeSerializer, CommentDisLikeSerializer
from .filters import HotelFilter, HotelMinRoomOrder

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework import filters


class CityHotelsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = HotelSerializer
    filter_backends = [DjangoFilterBackend, HotelMinRoomOrder, filters.OrderingFilter]
    filterset_class = HotelFilter
    ordering_fields = ['min_room_price', 'stars']

    def get_queryset(self):
        city_name = self.kwargs['city_name']
        return Hotel.objects.filter(city__name=city_name).distinct()

    @action(detail=True, methods=['POST'])
    def create_comment(self, request, *args, **kwargs):
        serializer = HotelCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        HotelComment.objects.create(user=self.request.user,
                                    hotel=validated_data['hotel'],
                                    content=validated_data['content'])
        return Response("comment created successfully")

    @action(detail=True, methods=['POST'])
    def like_comment(self, request, *args, **kwargs):
        serializer = CommentLikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        if CommentLike.objects.filter(user=self.request.user, comment=validated_data['comment']).exists():
            return Response("you already liked it")
        CommentLike.objects.create(user=self.request.user,
                                   comment=validated_data['comment'])
        return Response("you liked comment successfully")

    @action(detail=True, methods=['POST'])
    def dislike_comment(self, request, *args, **kwargs):
        serializer = CommentDisLikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        if CommentDisLike.objects.filter(user=self.request.user, comment=validated_data['comment']).exists():
            return Response('you already disliked it')
        CommentDisLike.objects.create(user=self.request.user,
                                      comment=validated_data['comment'])
        return Response("you disliked comment successfully")

    @action(detail=True, methods=['POST'])
    def like_hotel(self, request, *args, **kwargs):
        serializer = HotelLikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        if HotelLike.objects.filter(user=self.request.user, hotel=validated_data['hotel']).exists():
            return Response("you already liked it")
        HotelLike.objects.create(user=self.request.user,
                                 hotel=validated_data['hotel'])
        return Response("you liked hotel successfully")
    

class RoomViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    
class HomeViewSet(GenericViewSet):
    
    def list(self, request):
        kish_hotels = Hotel.objects.filter(city__name__icontains='کیش', stars=5)[:3]
        mashhad_hotels = Hotel.objects.filter(city__name__icontains='مشهد', stars=5)[:3]
        tehran_hotels = Hotel.objects.filter(city__name__icontains='تهران', stars=5)[:3]
        shiraz_hotels = Hotel.objects.filter(city__name__icontains='شیراز', stars=5)[:3]
        qeshm_hotels = Hotel.objects.filter(city__name__icontains='قشم', stars=5)[:3]
        isfahan_hotels = Hotel.objects.filter(city__name__icontains='اصفهان', stars=5)[:3]
        kish_serializer = HotelHomeSerializer(kish_hotels, many=True)
        mashhad_serializer = HotelHomeSerializer(mashhad_hotels, many=True)
        tehran_serializer = HotelHomeSerializer(tehran_hotels, many=True)
        shiraz_serializer = HotelHomeSerializer(shiraz_hotels, many=True)
        qeshm_serializer = HotelHomeSerializer(qeshm_hotels, many=True)
        isfahan_serializer = HotelHomeSerializer(isfahan_hotels, many=True)

        popular_hotels = Hotel.objects.all().annotate(num_likes=Count('likes')).order_by('-num_likes')[:3]
        popular_hotels_serializer = PopularHotelSerializer(popular_hotels, many=True)

        return Response({
            'kish_hotels': kish_serializer.data,
            'mashhad_hotels': mashhad_serializer.data,
            'tehran_hotels': tehran_serializer.data,
            'shiraz_hotels': shiraz_serializer.data,
            'qeshm_hotels': qeshm_serializer.data,
            'isfahan_hotels': isfahan_serializer.data,
            'popular_hotels': popular_hotels_serializer.data
        })
