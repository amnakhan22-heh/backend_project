from rest_framework.throttling import UserRateThrottle
#throttles user on the basis of ip or userid
class LoginThrottle(UserRateThrottle):
    rate = '5/min'