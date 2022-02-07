from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NoteSerializer
from .models import Note
from api import serializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        {
            'Endpoint': '/notes/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/notes/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new note with data sent in request'
        },
        {
            'Endpoint': '/notes/id/update',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing note with data sent in request'
        },
        {
            'Endpoint': '/notes/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes note'
        }
    ]
    return Response(routes)

@api_view(['GET'])    
def getNotes(request):
    notes = Note.objects.all()
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)

@api_view(['GET'])    
def getNote(request, pk):
    try:
        note = Note.objects.get(id=pk)
        serializer = NoteSerializer(note, many=False)
        return Response(serializer.data)
    except Note.DoesNotExist:
        return Response('Note not found', status=404)

@api_view(['POST'])
def createNote(request):
    try:
        data = request.data

        note = Note.objects.create(
            body=data['body'],
            title=data['title']
        )
        serializer = NoteSerializer(note, many=False)
        
        return Response(serializer.data)
    except KeyError:
        return Response('Invalid data', status=422)

@api_view(['PUT'])
def updateNote(request, pk):
    try:
        data = request.data

        note = Note.objects.get(id=pk)
        serializer = NoteSerializer(note, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
        
        return Response(serializer.data)
    except Note.DoesNotExist:
        return Response('Note youre trying to update does not exist', status=404)

@api_view(['DELETE'])
def deleteNote(request, pk):
    try:
        note = Note.objects.get(id=pk)
        note.delete()
        return Response('Note was deleted')
    except Note.DoesNotExist:
        return Response('Note you are trying to delete is not found', status=404)

    