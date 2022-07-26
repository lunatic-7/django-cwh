# I have created this file - Wasif

from ssl import Purpose
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


def analyze(request):
    # Get the text
    djtext = request.POST.get('text', 'default')

    # Check checkbox values
    removepunc = request.POST.get('removepunc', 'off')
    uppercase = request.POST.get('uppercase', 'off')
    newlineremover = request.POST.get('newlineremover', 'off')
    extraspaceremover = request.POST.get('extraspaceremover', 'off')
    charcount = request.POST.get('charcount', 'off')

    analyzed = ""
    purpose = ""
    # Check which checkbox is on
    if removepunc == "on":
        punctuations = '''!()-[]{/}};:'"\,<>./?@#$%^&*_~'''
        purpose += "| Remove Punctuations |"
        for char in djtext:
            if char not in punctuations:
                analyzed += char
        params = {
            'purpose': purpose,
            'analyzed_text': analyzed
        }

        djtext = analyzed

    if uppercase == "on":
        purpose += "| UPPERCASE |"
        analyzed = djtext.upper()
        params = {
            'purpose': purpose,
            'analyzed_text': analyzed
        }

        djtext = analyzed

    if newlineremover == "on":
        purpose += "| New Line Remover |"
        analyzed = ""
        for _ in djtext:
            if _ != "\n" and _ != "\r":
                analyzed += _
        params = {
            'purpose': purpose,
            'analyzed_text': analyzed
        }

        djtext = analyzed

    if extraspaceremover == "on":
        analyzed = ""
        purpose += "| Extra Space Remover |"
        for i, v in enumerate(djtext):
            if not(djtext[i] == " " and djtext[i + 1] == " "):
                analyzed += v
        params = {
            'purpose': purpose,
            'analyzed_text': analyzed
        }

        djtext = analyzed

    if charcount == "on":
        count = len(djtext)
        purpose += "| Character Counter |"
        params = {
            'purpose': purpose,
            'analyzed_text': f"{analyzed} \nYour count is: {count}",
        }

    if removepunc == "off" and uppercase == "off" and newlineremover == "off" and extraspaceremover == "off" and charcount == "off":
        params = {
            'purpose': 'No operation selected (ERROR)',
            'analyzed_text': djtext
        }
        return render(request, 'analyze.html', params)
    
    return render(request, 'analyze.html', params)
