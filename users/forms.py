from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .watermark import add_watermark
from datingapp.settings import BASE_DIR


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'gender', 'user_picture')

    # adding watermark to user picture
    def clean_user_picture(self):
        user_picture = self.cleaned_data['user_picture']
        watermark_path = BASE_DIR / 'users/static/users/images/watermark.png'
        picture_with_watermark = add_watermark(user_picture, watermark_path)
        return picture_with_watermark
