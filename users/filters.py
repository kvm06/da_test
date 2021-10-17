import django_filters
from .models import CustomUser, UserCoords
from .distance import get_distance_by_coords
from django.contrib.gis.geoip2 import GeoIP2
from django.core.exceptions import ObjectDoesNotExist

import math

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'gender']

        first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='startswith')
        second_name = django_filters.CharFilter(field_name='second_name', lookup_expr='startswith')
        gender = django_filters.CharFilter(field_name='gender', lookup_expr='exact')

    distance = django_filters.CharFilter(method = 'my_custom_filter', label="Расстояние")

    def my_custom_filter(self, queryset, id, value):
        "Фильтрация пользователей по расстоянию value. Возвращает всех пользователей, расстояние до которых меньше указанного значения"
        radius = int(value) 
        current_user = self.request.user #Текущий пользователь
        current_user_coords = UserCoords.objects.get(user=current_user) #Геокоординаты текущего пользователя
        users_in_radius = queryset # 
        for other_user in queryset:
            try:
                #Вычисляем координаты другого пользователя
                other_user_coords = UserCoords.objects.get(user=other_user)
                #Вычисляем расстояние до другого пользователя
                dist_between_users = get_distance_by_coords(current_user_coords, other_user_coords) 
                #Если расстояние больше заданного значения, исключаем пользователя
                if not dist_between_users or dist_between_users > radius:
                    users_in_radius = users_in_radius.exclude(id=other_user.id)
            except ObjectDoesNotExist:
                users_in_radius = users_in_radius.exclude(id=other_user.id)
        queryset = users_in_radius
        return queryset