from django.shortcuts import render

# Create your views here.
import google.generativeai as genai
from django.shortcuts import render, redirect
import random, os


GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

encouragements = [
    "You're doing amazing! 🌟",
    "We’re smashing this topic, GS! 💥",
    "Big brain energy 🔥🧠",
    "Keep rocking! 🎸",
]

def study_chat(request):
    if 'study_history' not in request.session:
        request.session['study_history'] = []

    if request.method == 'POST':
        user_input = request.POST.get('query')
        subject = request.POST.get('subject', 'General')
        quiz_mode = request.POST.get('quiz_mode', 'off') == 'on'
        dark = request.POST.get('dark', 'off') == 'on'

        prompt = f"""
        You're GS's AI study buddy named 'Buddy'. Be friendly, helpful, and fun.

        Subject: {subject}
        Quiz Mode: {'ON' if quiz_mode else 'OFF'}

        Question: {user_input}

        If Quiz Mode is ON, respond with 3-5 MCQs only.
        Otherwise, explain the concept casually, use emojis and encouragement.
        """

        response = format_response(model.generate_content(prompt).text.strip())

        response = response.replace("```", "<pre><code>").replace("```", "</code></pre>", 1)

        # response = format_response(response)  # 💡 Format before saving to session

        response += "\n\n" + random.choice(encouragements)

        request.session['study_history'].append({'sender': 'user', 'text': user_input})
        request.session['study_history'].append({'sender': 'bot', 'text': response})
        request.session['dark'] = dark
        request.session.modified = True

    return render(request, 'study.html', {
        'study_history': request.session.get('study_history', []),
        'dark': request.session.get('dark', False)
    })

def clear_chat(request):
    if 'study_history' in request.session:
        del request.session['study_history']
    return redirect('study_chat')


def format_response(text):
    import re
    # Convert ``` blocks to pre/code
    text = re.sub(r'```(?:\w+)?\n(.*?)```', r'<pre><code>\1</code></pre>', text, flags=re.DOTALL)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    return text

