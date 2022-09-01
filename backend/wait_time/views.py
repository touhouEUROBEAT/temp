from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from django.views import View
from rest_framework.response import Response
import redis
import ujson
import pprint

def index(request):
    return HttpResponse("Hello, world. You're at the wait time index.")

class wait_time_data(APIView):
    def get(self, request):
        # Changing how wait_time data is stored in redis to better serve Andrew's implementation

        # waitTimeList = []
        # r = redis.StrictRedis(host="132.249.242.203", port=6379, db=0, password='kungfurubberducky2022')
        # for key in r.scan_iter():
        #     if (key != None and 'wait'.encode() in key):
        #         place = ujson.loads(r.get(key))
        #         waitTimeList.append(place)
        # filteredList = []
        # for location in waitTimeList:
        #     filter = {
        #         "place" : location['name'],
        #         "capacityPercentage" : location['percentage'],
        #         "subLocation" : False
        #     }
        #     if (location['subLocs'] != False):
        #         filter['subLocation'] = location['subLocs']
        #     filteredList.append(filter)
        # return Response(filteredList)

        r = redis.StrictRedis(host="132.249.242.203", port=6379, db=0, password='kungfurubberducky2022')

        return Response(ujson.loads(r.get('wait_time')))

