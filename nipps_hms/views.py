from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class APIs(APIView):

    def get(self, request, *args, **kwargs):

        return Response({"message": "The NIPSS APIs",}, status=status.HTTP_200_OK)
        