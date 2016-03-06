from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse
import json
import models

def index(request):
    return HttpResponse("Hello. You're at the CubeApp index.")

@csrf_exempt
def createUser(request):
    if request.method == 'POST':
        user_dict = json.loads(request.body)
        if "name" in user_dict and "city" in user_dict:
            u = models.User.objects.create(name=user_dict["name"], city=user_dict["city"])
            created_user = {"id":u.id, "name":u.name, "city":u.city}
            return JsonResponse(created_user)
        else:
            message = "name or city missing in the request body"
    else:
        message = "Not a POST request. Can't create user"
    message_dict = {"message":message}
    return JsonResponse(message_dict)

@csrf_exempt
def createGetCube(request, user_id):
    if request.method == 'POST':
        cube_dict = json.loads(request.body)
        if "name" in cube_dict:
            user_query = models.User.objects.filter(id=user_id)
            if user_query.exists():
                c = models.Cube.objects.create(name = cube_dict["name"])
                c.users.add(user_query.first())
                created_cube = {"id":c.id, "name":cube_dict["name"], "user_id":user_id}
                return JsonResponse(created_cube)
            else:
                message = "User with id %s doesn't exist" %user_id
        else:
            message = "Cube name missing in request body"
    elif request.method == 'GET':
        user_query = models.User.objects.filter(id=user_id)
        if user_query.exists():
            user = user_query.first()
            cubes = user.cube_set.all()
            #print cubes
            cube_list=[]
            for cube in cubes:
                cube_list.append(cube.asDict())
            cubes_dict = {"data":cube_list}
            return JsonResponse(cubes_dict)
        else:
            message = "User with id %s doesn't exist" %user_id
    else:
        message = "Not a GET or POST request"
    message_dict = {"message":message}
    return JsonResponse(message_dict)

@csrf_exempt
def createGetContent(request, user_id):
    if request.method == 'POST':
        content_dict = json.loads(request.body)
        if "link" in content_dict:
            user_query = models.User.objects.filter(id=user_id)
            if user_query.exists():
                c = models.Content.objects.create(link = content_dict["link"])
                c.users.add(user_query.first())
                created_content = {"id":c.id, "link":content_dict["link"], "user_id":user_id}
                return JsonResponse(created_content)
            else:
                message = "User with id %s doesn't exist" %user_id
        else:
            message = "Content link missing in request body"
    elif request.method == 'GET':
        user_query = models.User.objects.filter(id=user_id)
        if user_query.exists():
            user = user_query.first()
            contents = user.content_set.all()
            content_set = set([])
            for content in contents:
                content_set.add(content)
            #print contents
            cubes = user.cube_set.all()
            for cube in cubes:
                c=cube.contents.all()
                #print c
                for content in c:
                    content_set.add(content)
            content_list=[]
            for content in content_set:
                content_list.append(content.asDict())
            return JsonResponse({"data":content_list})
        else:
            message = "User with id %s doesn't exist" %user_id
    else:
        message = "Not a GET or POST request"
    message_dict = {"message":message}
    return JsonResponse(message_dict)

@csrf_exempt
def addContentToCube(request, user_id, cube_id):
    if request.method == 'POST':
        if not models.User.objects.filter(id=user_id).exists():
            return HttpResponse("User with id %s doesnt exist" %user_id)
        cube_query = models.Cube.objects.filter(id=cube_id)
        if not cube_query.exists():
            return HttpResponse("Cube with id %s doesnt exist" %cube_id)
        if not cube_query.filter(users__id=user_id).exists():
            return HttpResponse("User id %s doesnt have access to Cube id %s" %(user_id, cube_id))
        content_dict = json.loads(request.body)
        if "content_id" in content_dict:
            content_id = int(content_dict["content_id"])
            content_query = models.Content.objects.filter(id=content_id)
            if content_query.exists():
                cube = cube_query.first()
                cube.contents.add(content_query.first())
                return JsonResponse({"cube_id":cube_id,"content_id":content_id})
            else:
                message="Content with id %s doesn't exist" %content_id
        else:
            message = "content_id missing in request body"
    else:
        message = "Not a POST request. Can't add content to cube"
    message_dict = {"message":message}
    return JsonResponse(message_dict)

@csrf_exempt
def deleteContentFromCube(request, user_id, cube_id, content_id):
    if request.method == 'DELETE':
        if not models.User.objects.filter(id=user_id).exists():
            return HttpResponse("User with id %s doesnt exist" %user_id)
        cube_query = models.Cube.objects.filter(id=cube_id)
        if not cube_query.exists():
            return HttpResponse("Cube with id %s doesnt exist" %cube_id)
        if not cube_query.filter(users__id=user_id).exists():
            return HttpResponse("User id %s doesnt have access to Cube id %s" %(user_id, cube_id))
        content_query = models.Content.objects.filter(id=content_id)
        if not content_query.exists():
            return HttpResponse("Content with id %s doesnt exist" %content_id)
        if not cube_query.filter(contents__id=content_id).exists():
            return HttpResponse("Content id %s doesn't exist in the Cube id %s" %(content_id, cube_id))
        cube_query.first().contents.remove(content_query.first())
        message = "Deletion Successful."
    else:
        message = "Not a DELETE request. Can't delete content from cube"
    message_dict = {"message":message}
    return JsonResponse(message_dict)

@csrf_exempt
def deleteCube(request, user_id, cube_id):
    if request.method == 'DELETE':
        if not models.User.objects.filter(id=user_id).exists():
            return HttpResponse("User with id %s doesnt exist" %user_id)
        cube_query = models.Cube.objects.filter(id=cube_id)
        if not cube_query.exists():
            return HttpResponse("Cube with id %s doesnt exist" %cube_id)
        if not cube_query.filter(users__id=user_id).exists():
            return HttpResponse("User id %s doesnt have access to Cube id %s" %(user_id, cube_id))
        cube = cube_query.first()
        cube.delete()
        message = "Deletion Successful."
    else:
        message = "Not a DELETE request. Can't delete cube"
    message_dict = {"message":message}
    return JsonResponse(message_dict)

@csrf_exempt
def shareCube(request, user_id, cube_id):
    if request.method == 'POST':
        if not models.User.objects.filter(id=user_id).exists():
            return HttpResponse("User with id %s doesnt exist" %user_id)
        cube_query = models.Cube.objects.filter(id=cube_id)
        if not cube_query.exists():
            return HttpResponse("Cube with id %s doesnt exist" %cube_id)
        if not cube_query.filter(users__id=user_id).exists():
            return HttpResponse("User id %s doesnt have access to Cube id %s" %(user_id, cube_id))
        user_dict = json.loads(request.body)
        if "user_id" in user_dict:
            uid=int(user_dict["user_id"])
            user_query = models.User.objects.filter(id=uid)
            if not user_query.exists():
                return HttpResponse("User(id:%d) with whom you want to share doesn't exist" %uid)
            cube=cube_query.first()
            cube.users.add(user_query.first())
            return JsonResponse({"cube_id":cube_id, "user_id":user_id})
        else:
            message = "user_id not in request body"
    else:
        message = "Not a POST request. Can't share Cube"
    message_dict = {"message":message}
    return JsonResponse(message_dict)

@csrf_exempt
def shareContent(request, user_id, content_id):
    if request.method == 'POST':
        if not models.User.objects.filter(id=user_id).exists():
            return HttpResponse("User with id %s doesnt exist" %user_id)
        content_query = models.Content.objects.filter(id=content_id)
        if not content_query.exists():
            return HttpResponse("Content with id %s doesnt exist" %content_id)
        if not content_query.filter(users__id=user_id).exists():
            return HttpResponse("User id %s doesnt have access to Content id %s" %(user_id, content_id))
        user_dict = json.loads(request.body)
        #print user_dict
        if "user_id" in user_dict:
            uid=int(user_dict["user_id"])
            user_query = models.User.objects.filter(id=uid)
            if not user_query.exists():
                return HttpResponse("User(id:%d) with whom you want to share doesn't exist" %uid)
            content=content_query.first()
            content.users.add(user_query.first())
            return JsonResponse({"content_id":content_id, "user_id":user_id})
        else:
            message = "user_id not in request body"
    else:
        message = "Not a POST request. Can't share Content"
    message_dict = {"message":message}
    return JsonResponse(message_dict)

"""
@csrf_exempt
def deleteAll(request):
    cubes = models.Cube.objects.all()
    for c in cubes:
        c.delete()
    contents = models.Content.objects.all()
    for c in contents:
        c.delete()
    return HttpResponse("sd")"""
