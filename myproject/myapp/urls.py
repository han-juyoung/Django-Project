from django.urls import path
from myapp import views

urlpatterns = [ #사용자가 원하는 링크로 이동 no2
   path('', views.index),
   path('create/', views.create),
   path('read/<id>/', views.read),  # 바뀔수 있는 값은 <>로 <>안에 이름 넣어줌
   path('update/<id>', views.update),
   path('delete/', views.delete),

]
# views 를 연결하고 싶으면 no3
