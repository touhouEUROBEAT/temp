from django.db import models

# Create your models here.

# Stores pending matchings. Once a matching is approved, move to All_matching
class PendingMatching(models.Model):
    id_sender = models.IntegerField()
    id_receiver = models.IntegerField()

    isDenied = models.BooleanField(default=False)

    # Do we need a timestamp?

    def __str__(self):
        return str(self.id_sender) + "-->" + str(self.id_receiver) + " isDenied: " + str(self.isDenied)


# Stores matchings that have been approved by both parties.
class FinalizedMatching(models.Model):
    id_user_1 = models.IntegerField()
    id_user_2 = models.IntegerField()

    # Do we need a timestamp?

    def __str__(self):
        return str(self.id_user_1) + "--" + str(self.id_user_2)