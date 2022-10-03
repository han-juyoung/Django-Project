from django.db import models

class BoardMember(models.Model):
    username    = models.CharField(max_length=100, verbose_name='사용자명') # admin에서 보일 컬럼명
    email       = models.EmailField(max_length=100, verbose_name='사용자메일')
    password    = models.CharField(max_length=100, verbose_name='사용자PW')
    re_password = models.CharField(max_length=100, verbose_name='사용자PW확인')
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='가입날짜')
    updated_at  = models.DateTimeField(auto_now=True, verbose_name='마지막수정일')

    def __str__(self):
        return self.username

    class Meta:
        db_table            = 'boardmembers'
        verbose_name        = '게시판멤버'
        verbose_name_plural = '게시판멤버'
