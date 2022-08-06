from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('Lists/', views.lists, name='File-Lists'),
    path('Upload/', views.upload, name="Upload"),
    path('Block/', views.block_file, name="file-block"),
    path('Unblock/', views.unblock_file, name='file-unblock'),
    path('Admin/', views.Admin, name='Admin'),
    path('upload/', FileUpload.as_view(), name='file-upload-api'),
    path('lists/', Lists.as_view(), name='list-files-api'),
    path('admin/', admin.as_view(), name='admin-api'),
    path('download/<int:id>/', FileDownload.as_view(), name="file-download-api"),
    path('file_block/<int:pk>/', views.file_block, name='file-blocking-request-api'),
    path('file_unblock/<int:pk>/', views.file_unblock, name='file-unblocking-request-api'),
    path('file_block_unblock/<int:pk>/', views.file_block_unblock, name="file-block-unblock-admin"),
    path('last_downloaded/<int:pk>/', views.last_download, name="last_downloaded")
]
