from zipapp import create_archive
from django.test import TestCase
from django.urls import reverse

from api.serializers import NoteSerializer
from .models import Note

# Create your tests here.

class URLTests(TestCase):

    def setUp(self):
        Note.objects.create(
            body={
                'title': 'title',
                'body': 'body',
            })

    def test_home(self):
        """Test home route"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_notes(self):
        """Test notes overview"""
        response = self.client.get(reverse('notes'))
        self.assertEqual(response.status_code, 200)
    
    def test_create_note(self):
        """Test note creation"""
        response = self.client.post(reverse('create_note'), data={
            'title': 'unique title',
            'body': 'body',
        }, content_type='application/json')
        note = Note.objects.filter(title='unique title')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(note)
        new_response = self.client.post(reverse('create_note'), data={
            'xx': 'unique title',
            'xx': 'body',
        }, content_type='application/json')
        self.assertEqual(new_response.status_code, 422)
        self.assertRaises(KeyError)
    
    def test_update_note(self):
        """Test note update"""
        note = Note.objects.get(id=1)
        oldTitle = note.title
        response = self.client.put(reverse('update_note', args=[note.id]), data={
            'title': 'new title',
        }, content_type='application/json')
        
        newTitle = Note.objects.get(id=1).title
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(oldTitle, newTitle)
        response = self.client.put(reverse('update_note', args=['100']))
        self.assertRaises(Note.DoesNotExist)
        self.assertEqual(response.status_code, 404)
    
    def test_delete_note(self):
        """Test note delete"""
        note = Note.objects.get(id=1)
        response = self.client.delete(reverse('delete_note', args=[note.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('get_note', args=[note.id]))
        self.assertEqual(response.status_code, 404)
        new_response = self.client.delete(reverse('delete_note', args=['100']))
        self.assertRaises(Note.DoesNotExist)
        self.assertEqual(response.status_code, 404)

    def test_get_note(self):
        """Test get note"""
        note = Note.objects.get(id=1)
        serialized_note = NoteSerializer(note, many=False)
        response = self.client.get(reverse('get_note', args=[note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serialized_note.data, response.data)
    
    def test_title_length(self):
        note = Note.objects.create(
            body='body',
            title='title'*20,
        )
        self.assertEqual(len(str(note)), 50)
