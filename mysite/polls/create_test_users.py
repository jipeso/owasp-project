from django.contrib.auth.models import User

def run():
  if not User.objects.filter(username='alice').exists():
      User.objects.create_user(username='alice', password='alice')
      print("created user: alice")

  if not User.objects.filter(username='bob').exists():
      User.objects.create_user(username='bob', password='bob')
      print("created user: bob")