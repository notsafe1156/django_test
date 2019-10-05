from RSS.models import Data
from RSS.serializers import DataSerializer
from RSS.models import fund_datas, update_text, dbget_info_min, verify_account, check_hash, delete_byid, getfulltext
from RSS.models import get_text_by_source_server, get_text_by_source_client, return_source

from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponseRedirect
import json


def hello(request):
    return render(request, 'test.html')


def index(request):
    return render(request, 'hompage/test.html')


class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

    # permission_classes = (IsAuthenticated,)

    @action(methods=['get'], detail=True)
    def aa(self, request, pk=None):
        print(pk)
        data = get_object_or_404(Data, pk=pk)
        result = {
            'id': data.id
        }

        return Response(result, status=status.HTTP_200_OK)

    # 測試用
    @action(methods=['get'], detail=False)
    def raw_sql_query(self, request):
        ida = request.query_params.get('id', None)
        test1 = fund_datas(id=ida)
        serializer = DataSerializer(test1, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 更新資料用
    @action(methods=['put'], detail=False)
    def update_text(self, request, pk=None):
        print(request.data)
        id = request.data.get('id')
        category = request.data.get('category')
        tag = request.data.get('tag')
        display = request.data.get('display')
        data = update_text(id=id, category=category, tag=tag, display=display)
        if data:
            result = '更新完成'
        else:
            result = '更新失敗'
        return Response(result, status=status.HTTP_200_OK)

    # 拿後臺主頁資料
    @action(methods=['post'], detail=False)
    def get_info_min(self, request):
        longin_hash = request.data.get('hash')
        account = request.data.get('account')
        print(str(longin_hash))
        if check_hash(account, longin_hash):
            print('------------')
            data = dbget_info_min()
            return Response(data, status=status.HTTP_200_OK)
        print('+++++++++++++')
        return Response(False, status=status.HTTP_200_OK)

    # 弄做登入用，輸入正確傳回帳號做hash
    @action(methods=['post'], detail=False)
    def login(self, request):
        account = request.data.get('account')
        password = request.data.get('password')
        result = verify_account(account=account, password=password)
        if result:
            result = str(result)
        return Response(result, status=status.HTTP_200_OK)

    # 測試用
    @action(methods=['get'], detail=False)
    def request_test(self, request):
        return HttpResponseRedirect('https://ffbd6e99.ngrok.io/templates/test2')

    # 刪除
    @action(methods=['delete'], detail=False)
    def delete(self, request):
        id = request.data.get('id')
        print(request.data)
        print(id)
        print(type(id))
        result = delete_byid(id)
        if result:
            result = '刪除成功:' + str(id)
        else:
            result = '刪除失敗'
        return Response(result, status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def get_text(self, request):
        id = request.query_params.get('id', None)
        result = getfulltext(id=id)
        return Response(result, status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def return_by_source(self, request):
        source = request.query_params.get('source', None)
        result = get_text_by_source_server(source)
        return Response(result, status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def get_text_by_source(self, request):
        source = request.query_params.get('source', None)
        result = get_text_by_source_client(source)
        return Response(result, status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def get_source(self, request):
        result = return_source()
        return Response(result, status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def get_info_for_page(self, request):
        page = request.query_params.get('pages',None)
        


