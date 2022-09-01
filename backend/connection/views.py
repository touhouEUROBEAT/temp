from re import TEMPLATE
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.authentication import TokenAuthentication

from account.models import Student
from account.LISTS import *
from account.serializer import StudentSerializer
from api.serializers import *
from .models import *

from account.helpers import redis_get_student, redis_set_student, redis_get_attrib
from connection.helpers import get_pfp
import random
import ujson
import time
import redis

from .word_vec import *

#from embeddings import GloveEmbedding

# from numba import jit
from multiprocessing import Pool


# Create your views here.

class GetInfo(APIView):
    authentication_classes = [TokenAuthentication]

    # To get info for user that's currently logged in
    def get(self, request):

        r = redis.StrictRedis(host="132.249.242.203", port=6379, db=0, password='kungfurubberducky2022')
        pipe = r.pipeline()

        if (request.user.is_authenticated):
            temp = redis_get_student(r, pipe, request.user.id)

            print(redis_get_attrib(r, request.user.id))

            temp.update(redis_get_attrib(r, request.user.id))
            return Response(temp)
        else:
            return Response({})

class GetPFPView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        start_time = time.time()

        if (request.user.is_authenticated):
            print("Below is pfp time")
            print("--- %s seconds ---" % (time.time() - start_time))
            return Response(get_pfp(request.user.id))
        else:
            return Response({})

    def post(self, request):
        request_content = ujson.loads(request.body.decode("utf-8"))
        print(request_content)

        start_time = time.time()

        if (request.user.is_authenticated):

            print("Below is pfp time")
            print("--- %s seconds ---" % (time.time() - start_time))
            return Response(get_pfp(request_content['id']))

            #temp = redis_get_student(r, pipe, request_content['id'])
            #temp.update(redis_get_attrib(r, request_content['id']))
            #return Response(temp)

        else:
            return Response({})


class GetInfoTest(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        toRespond = StudentSerializer(Student.objects.get(pk=1)).data
        return Response(toRespond)

    # To get info of any user given uid
    def post(self, request):
        request_content = ujson.loads(request.body.decode("utf-8"))
        #print(request_content['id']);

        r = redis.StrictRedis(host="132.249.242.203", port=6379, db=0, password='kungfurubberducky2022')
        pipe = r.pipeline()

        if (request.user.is_authenticated):
            return Response(redis_get_student(r, pipe, request_content['id']))
        else:
            return Response({})


# 地図: AddKarmaView API
class AddKarmaView(APIView):
    def post(self, request):
        request_content = ujson.loads(request.body)

        # Get the user id so we can use to find the User object
        request_user_id = request_content.get("user_id")

        #Open connection to Redis
        r = redis.StrictRedis(
            host="132.249.242.203", port=6379, db=0, password='kungfurubberducky2022')
        pipe = r.pipeline()

        # Find Student with specified request_user_id
        temp = redis_get_student(r, pipe, request_user_id)

        add_karma = temp.get("user_karma") + request_content.get("add_karma");

        temp.update({'user_karma': add_karma})

        redis_set_student(r, request_user_id, temp)

        student = Student.objects.get(id=request_user_id)
        student.user_karma = temp.get('user_karma');
        student.save();

        return Response({})


# Placeholder before we have a real matching algo


'''
    Tons of room for optimization, but will do for now.
'''

'''
    GET: Fetches all Matching that has been sent out.
'''


class MatchingSentView(APIView):
    # print("MatchingSentView has been called");

    authentication_classes = [TokenAuthentication]

    def get(self, request):
        start_time = time.time()
        matching_sent = list(PendingMatching.objects.filter(id_sender=request.user.id))

        toReturn = []
        r = redis.StrictRedis(host="132.249.242.203", port=6379, db=0, password='kungfurubberducky2022')
        pipe = r.pipeline()

        for i in matching_sent:
            # No longer needed now that we have Student as wrapper model
            # temp = helpers.conn_wrapper(User.objects.get(pk=i.id_receiver), Student.objects.get(pk=i.id_receiver))

            temp = redis_get_student(r, pipe, i.id_receiver)
            temp.update({'isDenied': i.isDenied})

            toReturn.append(temp)

        pipe.execute()

        # print("--- %s seconds ---" % (time.time() - start_time))
        return Response(toReturn)


'''
    GET: Fetches all Matching that has been received.
'''


# TODO: try out multi-threading
class MatchingReceivedView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        matching_received = list(PendingMatching.objects.filter(id_receiver=request.user.id))

        r = redis.StrictRedis(host="132.249.242.203", port=6379, db=0, password='kungfurubberducky2022')
        pipe = r.pipeline()
        toReturn = []

        for i in matching_received:
            temp = redis_get_student(r, pipe, i.id_sender)
            temp.update({'isDenied': i.isDenied})

            toReturn.append(temp)

        pipe.execute()

        return Response(toReturn)


'''
    GET: Fetches all Matching that has been sent out.
    POST: Sends out a request for the matching generated
'''


class GenerateMatchingView(APIView):
    authentication_classes = [TokenAuthentication]

    # TO-DO: User shown before and after request do not match (match request is sent to user shown before, but a different user is shown when match is pending )
    # If front end makes a GET request to url associated to generate_match,
    # the func below executes
    def get(self, request):
        # Make sure the match is not the user itself

        #print("hello from get")
        temp = generate_match(request)
        #print(generate_match(request))
        #will have to do this on cloud instance
        # g = GloveEmbedding('common_crawl_840', d_emb=300, show_progress=True)
        print("DONE")

        # Send the information about the match back to the front end
        if temp:
            return Response(StudentSerializer(Student.objects.get(pk=temp.id)).data)
        else:
            return Response({})

    # If front end makes a POST request to url associated to generate_match,
    # the func below executes
    def post(self, request):
        #print("hello from post")
        #print(request.user)

        # Extract
        request_content = ujson.loads(request.body)

        # Create a new PendingMatching object, where the sender and receivers are as specified by our input
        m = PendingMatching(
            id_sender=request.user.id,
            id_receiver=request_content.get("id_receiver"))

        # Insert the new PendingMatching object into database by calling .save()
        m.save()

        return Response({})


'''
    GET: Fetches all Matching that has been finalized.
'''


class MatchingFinalized(APIView):
    authentication_classes = [TokenAuthentication]

    # We may be able to optimize this by introducing a hashing mechanism.
    def get(self, request):
        finalized_matching = []

        r = redis.StrictRedis(host="132.249.242.203", port=6379, db=0, password='kungfurubberducky2022')
        pipe = r.pipeline()

        temp = FinalizedMatching.objects.filter(id_user_1=request.user.id)

        # our user is either user_1 or user_2, so we go through both lists
        for i in temp:
            finalized_matching.append(redis_get_student(r, pipe, i.id_user_2))

        temp = FinalizedMatching.objects.filter(id_user_2=request.user.id)
        for i in temp:
            finalized_matching.append(redis_get_student(r, pipe, i.id_user_1))

        pipe.execute()

        return Response(finalized_matching)


'''
    POST: Modify a pending matching by either:
        1. Accepting it and pushing it to the finalized table (mode: 'y')
        2. Denying it and marking it as denied (mode: 'n')
        3. Pulling it back / removing it at the user's discretion e.g. already denied (mode: 'd')
'''


class ModifyPending(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        request_content = ujson.loads(request.body);

        # print("request_content: ")
        # print(request_content)

        # If yes, push the matching into finalized matching
        # Only receiver could make this call, so request.user.id = id_receiver
        if (request_content.get("mode") == 'y'):
            # print("_____YAY_____");
            FinalizedMatching(id_user_1=request_content.get("id_sender"),
                              id_user_2=request.user.id).save()

            PendingMatching.objects.get(id_sender=request_content.get("id_sender"),
                                        id_receiver=request.user.id).delete()

        # If no, mark as denied. Only show to sender.
        # Only receiver could make this call, so request.user.id = id_receiver
        elif (request_content.get("mode") == 'n'):
            # print("_____NAY_____");
            p = PendingMatching.objects.get(id_sender=request_content.get("id_sender"),
                                            id_receiver=request.user.id)
            p.isDenied = True
            p.save()

        # Should we allow people to pullback pending matching?
        # Assuming we do, then this is visible to both sender and receiver
        # So we need to determine what request.user.id is.
        elif (request_content.get("mode") == 'd'):
            # Let front end supply only one id, and we can guess the other
            if (request_content.get("id_sender")):
                PendingMatching.objects.get(id_sender=request_content.get("id_sender"),
                                            id_receiver=request.user.id).delete()
            else:
                PendingMatching.objects.get(id_sender=request.user.id,
                                            id_receiver=request_content.get("id_receiver")).delete()

        return Response({})


# Placeholder before we have a real matching algo
# TODO: Conditions for matching
def generate_match(request):
    r = redis.StrictRedis(host="132.249.242.203", port=6379, db=0, password='kungfurubberducky2022')


    unavailable_id = get_unavailable_id(request)

    my_student = redis_get_student(r, r.pipeline(), request.user.id)
    my_interest = [my_student['user_interest1'], my_student['user_interest2'], my_student['user_interest3']]
    my_attrib = calc_attrib(interests=my_interest)

    tot_users = Student.objects.exclude(pk__in = unavailable_id).order_by('?')[:5]

    if (not tot_users):
        return None

    min_diff = 100
    min_user = None
    for i in tot_users:
        if i.id == request.user.id:
            continue

        cur_diff = 0
        cur_attrib = redis_get_attrib(r, i.id)
        for j in my_attrib.keys():
            cur_diff += abs(my_attrib[j] - cur_attrib[j])

        print(cur_diff)

        if cur_diff < min_diff:
            min_diff = cur_diff
            min_user = i

    print(min_user, min_diff)
    return min_user


# Helper functions

# returns tuple of the form (matching_sent, matching_received)
def get_pending_matching(request):
    matching_sent_id = PendingMatching.objects.filter(id_sender=request.user.id)
    matching_sent = []
    for i in matching_sent_id:
        matching_sent.append(Student.objects.get(pk=i.id_receiver))

    matching_received_id = PendingMatching.objects.filter(id_receiver=request.user.id)
    matching_received = []
    for i in matching_received_id:
        matching_received.append(Student.objects.get(pk=i.id_sender))

    return matching_sent, matching_received


# returns id of all pending matching a user has
def get_unavailable_id(request):
    temp = []

    for i in PendingMatching.objects.filter(id_sender=request.user.id):
        temp.append(i.id_receiver)

    for i in PendingMatching.objects.filter(id_receiver=request.user.id):
        temp.append(i.id_sender)

    for i in FinalizedMatching.objects.filter(id_user_1=request.user.id):
        temp.append(i.id_user_2)

    for i in FinalizedMatching.objects.filter(id_user_2=request.user.id):
        temp.append(i.id_user_1)

    return temp
