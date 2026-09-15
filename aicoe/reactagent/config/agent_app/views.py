from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .agent import run_agent


class ChatView(APIView):

    def post(self, request):

        session_id = request.data.get(
            "session_id"
        )

        message = request.data.get(
            "message"
        )

        if not session_id:

            return Response(
                {
                    "error": "session_id is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not message:

            return Response(
                {
                    "error": "message is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            result = run_agent(
                session_id=session_id,
                user_message=message
            )

            return Response(
                {
                    "session_id": session_id,
                    **result
                }
            )

        except Exception as exc:

            return Response(
                {
                    "error": str(exc)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Create your views here.
