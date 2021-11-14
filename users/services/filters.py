import django_filters
from users.models import CustomUser
from users.services.distance import get_distance


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'gender']

        first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='startswith')
        second_name = django_filters.CharFilter(field_name='second_name', lookup_expr='startswith')
        gender = django_filters.CharFilter(field_name='gender', lookup_expr='exact')

    distance = django_filters.CharFilter(method='radius_filter', label="Пользователи рядом")

    def radius_filter(self, queryset, name, value):
        """Find users in radius. Filter all users in radius <= value"""
        radius = int(value)
        lat, lng = self.request.user.lat, self.request.user.lng
        if lat and lng:
            all_users = CustomUser.objects.filter(is_admin=False)
            near_user_ids = [user.id for user in all_users if user.lat and user.lng and
                             get_distance(lat, lng, user.lat, user.lng) <= radius]
        else:
            return queryset
        return all_users.filter(id__in=near_user_ids)
