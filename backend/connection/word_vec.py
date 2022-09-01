from api.serializers import StudentSerializer
from account.models import Student

from django.apps import apps

import ujson
import redis

ATTRIB = ('introvert', 'foody', 'chad', 'athletic', 'academic', 'UCSD')

def calc_attrib(glove, interests, attrib):
    toReturn = dict.fromkeys(attrib)

    for i in attrib:
        emb_attrib = glove.emb(i)
        for j in interests:
            emb_interest = glove.emb(j)

            temp = 0
            for k in range(len(emb_interest)):
                temp += emb_attrib[k] * emb_interest[k]

        toReturn[i] = temp

    return toReturn
