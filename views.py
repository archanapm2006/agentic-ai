import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import run_react_agent

def index(request):
    """Renders the main dashboard HTML page."""
    return render(request, 'agent_app/index.html')

@csrf_exempt
def run_agent(request):
    """Handles AJAX requests from index.html and runs the ReAct agent."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_query = data.get('query', '')

            # Call your agent service execution function
            result = run_react_agent(user_query)

            # Ensure result is a dictionary before calling .get()
            if not isinstance(result, dict):
                result = {'final_answer': str(result)}

            return JsonResponse({
                'thought': result.get('thought', 'N/A'),
                'action': result.get('action', 'N/A'),
                'observation': result.get('observation', 'N/A'),
                'final_answer': result.get('final_answer', 'N/A')
            })
        except Exception as e:
            print("AGENT EXECUTION ERROR:", str(e))
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)