from django.test import TestCase
from .models import Account, Profile
from revoke import *

class AccountTest(TestCase):
    def get_accounts(self):
        revoke_by_leader_dict = {}
        leaders = Profile.objects.all()
        for leader in leaders:
            l = revoke_by_user(leader.user)
            revoke_by_leader_dict[leader] =  l
        return revoke_by_leader_dict

print(AccountTest.get_accounts("self"))
print("hello world")

# Create your tests here.
