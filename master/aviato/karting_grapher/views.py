from json import load
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .graph_generator import generate_graph


# Create your views here.

def karting_home(request):
    template = loader.get_template('karting_grapher/karting_grapher.html')
    return HttpResponse(template.render({},request))

def karting_add_new_time(request):
    if request.method == 'POST':
        #the user is trying to push its time to the server
        #start generating the graph
        uploaded_file = request.FILES['user_file']
        lines = uploaded_file.read().splitlines()
        lines_decoded = [k.decode("utf-8-sig") for k in lines]
        plot = generate_graph(lines_decoded)
        context = {
            'graph':plot
        }
        template = loader.get_template('karting_grapher/show_graph.html')
        return HttpResponse(template.render(context,request))

    else:
        template = loader.get_template('karting_grapher/add_new_data.html')
        return HttpResponse(template.render({},request))

def remove_begin_line_encoding(line):
    #remove the first two elements
    print(line[0:1],"This should be the first two elements")
    print("b\'","and this is what we want to remove")
    if line[0:1] == "b\'":
        line = line[2:]
        #if there was a begin line encoding we should also remove the ' at the end of it
        line = line[:-1]
    return line
        