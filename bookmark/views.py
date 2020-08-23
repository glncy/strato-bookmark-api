# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Bookmark, Tags
from rest_framework import viewsets
from django.db.models import Q
from functools import reduce
import ast

class BookmarkApiView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id', 'none')
        allBookmarks = Bookmark.objects
        if id != "none":
            specificBookmarks = allBookmarks.filter(id=id).values()
            if (len(specificBookmarks) > 0):
                return Response({ "status": "success", "message": "Found a Bookmark", "result": specificBookmarks })
            else:
                return Response({ "status": "failed", "message": "No Bookmark Found" })
        else:
            if 'search' in request.query_params:
                if 'tags' in request.query_params:
                    tags = request.query_params['tags'].split(",")
                    if (len(tags) > 0):
                        allBookmarks = allBookmarks.filter(Q(name__contains=request.query_params['search']) & reduce(lambda x, y: x | y, [Q(tags__contains=item) for item in tags]))
                    else: 
                        allBookmarks = allBookmarks.filter(name__contains=request.query_params['search'])
                else:
                    allBookmarks = allBookmarks.filter(name__contains=request.query_params['search'])
                if 'oldFirst' in request.query_params:
                    if request.query_params['oldFirst'] != "true":
                        allBookmarks = allBookmarks.order_by('-id')
                else:
                    allBookmarks = allBookmarks.order_by('-id')
            else:
                if 'tags' in request.query_params:
                    tags = request.query_params['tags'].split(",")
                    if (len(tags) > 0):
                        allBookmarks = allBookmarks.filter(reduce(lambda x, y: x | y, [Q(tags__contains=item) for item in tags]))
                    else: 
                        allBookmarks = allBookmarks.all()
                else:
                    allBookmarks = allBookmarks.all()
                if 'oldFirst' in request.query_params:
                    if request.query_params['oldFirst'] != "true":
                        allBookmarks = allBookmarks.order_by('-id')
                else:
                    allBookmarks = allBookmarks.order_by('-id')
            allBookmarks = allBookmarks.values()
            if (len(allBookmarks) > 0):
                return Response({ "status": "success", "message": "List of Bookmarks.", "result": allBookmarks })
            else:
                return Response({ "status": "failed", "message": "No Bookmarks" })

    def post(self, request, *args, **kwargs):
        id = kwargs.get('id', 'none')
        if id == "none":
            Bookmark.objects.create(
                name = request.data['name'],
                url = request.data['url'],
                tags = request.data['tags']
            )
            if len(request.data['tags']) > 0:
                for tag in request.data['tags']:
                    getTag = Tags.objects.all().filter(name__contains=tag).values()
                    if len(getTag) == 0:
                        Tags.objects.create(
                            name = tag.lower()
                        )
            id = Bookmark.objects.last()
            bookmark = Bookmark.objects.all().filter(id=id.pk).values()
            return Response({ "status": "success", "message": "New Bookmark Added.", "result": bookmark })
        else:
            return Response({ "status": "error", "message": "Invalid Request." })

    def put(self, request, *args, **kwargs):
        id = kwargs.get('id', 'none')
        if id != "none":
            result = Bookmark.objects.filter(id=id).update(
                name = request.data['name'],
                url = request.data['url']
            )
            if result > 0:
                return Response({ "status": "success", "message": "Updated the Information."})
            else:
                return Response({ "status": "failed", "message": "Unexpected Error Occur."})
        else:
            return Response({ "status": "error", "message": "Invalid Request." })
    
    def delete(self, request, *args, **kwargs):
        id = kwargs.get('id', 'none')
        if id != "none":
            bookmark = Bookmark.objects.filter(id=id).values()
            tags = ast.literal_eval(bookmark[0]['tags'])
            result = Bookmark.objects.filter(id=id).delete()
            if len(tags) > 0:
                for tag in tags:
                    getBookmarks = Bookmark.objects.filter(tags__contains=tag).values()
                    if len(getBookmarks) == 0:
                        Tags.objects.filter(name=tag.lower()).delete()
            if result[0] > 0:
                return Response({ "status": "success", "message": "Deleted the Information."})
            else:
                return Response({ "status": "failed", "message": "Unexpected Error Occur."})
        else:
            return Response({ "status": "error", "message": "Invalid Request." })

class TagApiView(APIView):
    def get(self, request, *args, **kwargs):
        tags = Tags.objects.all().values()
        if len(tags) > 0:
            return Response({ "status": "success", "message": "List of Tags.", "result": tags })
        else:
            return Response({ "status": "failed", "message": "No Available Tags."})