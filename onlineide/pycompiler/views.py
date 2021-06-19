import os
import sys
import uuid
import subprocess

from django.shortcuts import render


def home(request):
    if not os.path.exists('src'):
        os.mkdir('src')
    if request.method == 'POST':
        code = request.POST['codearea']
        try:
            stdout = sys.stdout
            filename = os.path.join('src', uuid.uuid4().hex + '.txt')
            sys.stdout = open(filename, 'w')
            exec(code)
            sys.stdout.close()
            output = open(filename, 'r').read()
        except BaseException as e:
            output = str(e)
            print(sys.exc_info())
            print(e.with_traceback(sys.exc_info()[2]))
            stdout = sys.stdout
        finally:
            if os.path.exists(filename):
                os.remove(filename)
            sys.stdout = stdout
            return render(request, 'home.html', {'code': code, 'output': output})
    return render(request, 'home.html')
