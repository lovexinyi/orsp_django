from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from orsp_django import settings
import uuid
from file.models import *
from user.models import *
import json
# Create your views here.
def uploadFile(request):
    # 此处可以接收文件和字符串
    f1 = request.FILES['usericon']
    print(f1)
    # 文件名
    filename=str(uuid.uuid4())+'.'+f1.name.split('.')[1]
    fname = '{0}/pic/{1}'.format(settings.STATICFILES_DIRS[0],filename)
    '''
    fname = '%s/pic/%s' % (settings.STATICFILES_DIRS[0], str(uuid.uuid4())+'.'+f1.name.split('.')[1])
    '''
    print(fname)
    with open(fname, 'wb') as pic:
        for c in f1.chunks():
            pic.write(c)
    return JsonResponse({
        "name":filename
    })

# 设置保存的文件名
def saveFile(request):
    print(json.loads(request.body))
    data=json.loads(request.body)
    print("data",data)
    res=Resource.objects.create(**data)
    return HttpResponse("ok")
# 下载文件
def downloadFile(request):
    if request.method == 'POST':
        try:
            # 此处可以接收文件和字符串
            f1 = request.FILES['usericon']
            usrid = request.POST.get('userid')
            # 设置保存的文件名
            fname = '%s/pic/%s' % (settings.STATICFILES_DIRS[0], f1.name)
            # 由于文件是二进制流的方式，所有要用chunks()
            with open(fname, 'wb') as pic:
                for c in f1.chunks():
                    pic.write(c)
            return JsonResponse({"code": "808"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})

# 取消上传的文件
def cancelfile(request):
    pass

# 查看文件信息(包括文件名,被下载次数,上传人,评论信息) 传过来一个资源id
def showfile(request):
    if request.method=="GET":
        resource_id=request.GET.get("id")
        res=Resource.objects.filter(id=resource_id).values("name","download_count","upload_user","describe")
        res=list(res)
        filename=res[0]["name"]
        download_count=res[0]["download_count"]
        user_id=res[0]["upload_user"]
        user_name = list(Info.objects.filter(id=user_id).values("user_name"))[0]["user_name"]
        describe=res[0]["describe"]
        file={
            "filename":filename,
            "download_count":download_count,
            "upload_user":user_name,
            "describe":describe
        }
        print(file)
        return JsonResponse({"file":file})

# 评论资源功能
def commentFile(request):
   pass

# 添加收藏 传过来用户的telephone和要收藏资源的id
def addCollect(request):
    if request.method=="GET":
        resource_id=request.GET.get('id')  # 被收藏资源的id
        tel=request.GET.get('telephone')  # 用户的电话号，要根据用户的电话号查到该用户的id
        user_id=list(User.objects.filter(telephone=tel).values("id"))[0]["id"]
        data = {
            "user_id": user_id,
            "resource_id": resource_id
        }
        print(data)
        res=Collect.objects.filter(user_id=user_id)
        if not res:
            Collect.objects.create(**data) # 向Collect用户收藏表添加数据
            return JsonResponse({"code":"209"}) # 收藏成功
        else:
            return HttpResponse("已收藏过了")
    else:
        return JsonResponse({"code":"404"})

# 取消收藏
def cancelCollect(request):
    if request.method == "GET":
        tel = request.GET.get('telephone')  # 用户的电话号，要根据用户的电话号查到该用户的id
        user_id = list(User.objects.filter(telephone=tel).values("id"))[0]["id"] # 用户id
        data = {
            "user_id": user_id,
        }
        res = Collect.objects.filter(user_id=user_id)
        print(data)
        if res:
            Collect.objects.filter(user_id=user_id).delete() # 向Collect用户收藏表添加数据
            return JsonResponse({"code": "222"})  # 取消收藏成功
        else:
            return HttpResponse("还没有收藏呢")
    else:
        return JsonResponse({"code": "404"})

# 检测文件重复(根据标题) 传过来一个title
def detectionRepetition(request):
    if request.method=="GET":
        title=request.GET.get("title")
        res=Resource.objects.filter(title=title)
        if res:
            return HttpResponse("文件重复")
        else:
            return HttpResponse("文件不重复")
            # return JsonResponse({"code":"250"}) # 文件不重复

# 点赞（根据资源id）
def like(request):
    if request.method=="GET":
        resource_id=request.GET.get('id')  # 资源的id
        like_num = Resource.objects.filter(id=resource_id).values("like_num")  # 查询结果为对象集合
        like_num = list(like_num)[0]["like_num"]  # 点赞数
        new_like_num = like_num + 1  # 点赞数+1
        print(resource_id, like_num, new_like_num)
        res = Resource.objects.filter(id=resource_id).update(like_num=new_like_num)  # 更新点赞数
        return JsonResponse({"like_num": new_like_num})  # 返回点赞数
    else:
        return JsonResponse({"code": "404"})