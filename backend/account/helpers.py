from api.serializers import StudentSerializer
from account.models import Student

from connection.word_vec import *

from django.apps import apps

import ujson
import redis


def redis_get_student(r, pipe, id):
    try:
        student = ujson.loads(r.get(f"student_{id}"))
    except:
        student = StudentSerializer(Student.objects.get(pk=id)).data
        pipe.set(f"student_{id}", ujson.dumps(student))

    return student


def redis_set_student(r, id, temp):
    # Idk why below isn't working but w/ temp it works so
    # student = StudentSerializer(temp).data
    r.set(f"student_{id}", ujson.dumps(temp))

    return temp


def redis_get_attrib(r, id):
    try:
        temp = ujson.loads(r.get(f"attrib_{id}"))
    except:
        student = StudentSerializer(Student.objects.get(pk=id)).data
        attribs = [student['user_interest1'], student['user_interest2'], student['user_interest3']]

        temp = calc_attrib(attribs)

        r.set(f"attrib_{id}", ujson.dumps(temp))

    return temp


def redis_set_attrib(r, id, temp):
    r.set(f"attrib_{id}", ujson.dumps(temp))

    return temp
