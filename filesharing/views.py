import hashlib
import mimetypes
import os
from datetime import datetime
from wsgiref.util import FileWrapper

from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.encoding import smart_str
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from datenbanken import settings
from .apps import my_session
from .serializers import *


def add_hash():
    last_id = File.objects.last().id
    last_file = File.objects.get(pk=last_id)
    file_path = last_file.file.path
    file_hash = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(file_hash.block_size)
            if not chunk:
                break
            file_hash.update(chunk)
    url = "https://www.tu-chemnitz.de/informatik/DVS/blocklist/" + file_hash.hexdigest()
    req = my_session.get(url)
    st_code = (int)(req.status_code)
    if st_code == 200:
        my_session.put(url)
    else:
        File.objects.filter(pk=last_id).update(blocking_status=True)
    File.objects.filter(pk=last_id).update(hash=file_hash.hexdigest())


def index(request):
    return redirect('/Lists/')


def Admin(request):
    return render(request, 'admin.html')


def lists(request):
    return render(request, 'file_lists.html')


def upload(request):
    return render(request, 'upload.html')


def block_file(request):
    return render(request, 'block_file.html')


def unblock_file(request):
    return render(request, 'unblock_file.html')


class FileUpload(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.validated_data['url'] = "http://127.0.0.1:8000/uploads/" + file_serializer.validated_data[
                'file'].name
            file_serializer.validated_data['size'] = file_serializer.validated_data['file'].size
            if file_serializer.validated_data['file'].size > 10 * 1024 * 1024:
                return HttpResponse('File too large. Size should not exceed 10 MiB.')
            else:
                file_serializer.save()
                add_hash()
                return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Lists(APIView):
    def get(self, request):
        queryset = File.objects.all()
        serializer = FileSerializer(queryset, many=True)
        return Response(serializer.data)


class FileDownload(APIView):
    def get(self, request, id, format=None):
        try:
            file = File.objects.get(pk=id)
            file_name = file.file.name
            file_path = settings.MEDIA_ROOT + '/' + file_name
            file_wrapper = FileWrapper(open(file_path, 'rb'))
            file_mimetype = mimetypes.guess_type(file_path)
            response = HttpResponse(file_wrapper, content_type=file_mimetype)
            response['X-Sendfile'] = file_path
            response['Content-Length'] = os.stat(file_path).st_size
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
            return response
        except File.DoesNotExist:
            return JsonResponse({'message': 'The file id  do not exists'},
                            status=status.HTTP_404_NOT_FOUND)



@api_view(['PUT'])
def file_block(request, pk):
    try:
        file = File.objects.get(pk=pk, blocking_status=False)
    except File.DoesNotExist:
        return JsonResponse({'message': 'The file does not exist or File is already blocked'},
                            status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        file_serializer = FileSerializer(file, data=request.data)
        if file_serializer.is_valid():
            file_serializer.validated_data['request_accept'] = True
            file_serializer.save()
            return JsonResponse(file_serializer.data)
        return JsonResponse(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def file_unblock(request, pk):
    try:
        file = File.objects.get(pk=pk, blocking_status=True)
    except File.DoesNotExist:
        return JsonResponse({'message': 'The file does not exist or File is already unblocked'},
                            status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        file_serializer = FileSerializer(file, data=request.data)
        if file_serializer.is_valid():
            file_serializer.validated_data['request_accept'] = True
            file_serializer.save()
            return JsonResponse(file_serializer.data)
        return JsonResponse(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def last_download(request, pk):
    try:
        file = File.objects.get(pk=pk)
        file.last_downloaded = datetime.now()
        file.save()
        return JsonResponse({'message': 'The file last downloaded time recorded'})
    except File.DoesNotExist:
        return JsonResponse({'message': 'The file does not exist or File is already unblocked'},
                            status=status.HTTP_404_NOT_FOUND)


class admin(APIView):
    def get(self, request):
        try:
            queryset = File.objects.filter(request_accept=True)
            authentication_classes = [BasicAuthentication]
            permission_classes = [IsAdminUser]
            serializer = FileSerializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return JsonResponse({'message': 'There is no request'},
                                status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def file_block_unblock(request, pk):
    if request.method == 'PUT':
        try:
            file = File.objects.get(pk=pk)
            if file.blocking_status == True:
                file.blocking_status = False
            else:
                file.blocking_status = True
            file.request_accept = False
            file.save()
            return JsonResponse({'message': 'File successfully blocked or unblock'})
        except File.DoesNotExist:
            return JsonResponse({'message': 'The file does not exist or File is already blocked or unblock'},
                                status=status.HTTP_404_NOT_FOUND)
