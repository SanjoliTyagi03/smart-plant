from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
import io

from plants.gemini import analyze_plant_image


class GeminiHelperTests(TestCase):

    def _mock_gemini_response(self, json_str):
        mock_response = MagicMock()
        mock_response.text = json_str
        return mock_response

    @patch('plants.gemini.genai')
    def test_analyze_returns_structured_dict(self, mock_genai):
        fake_json = '''{
            "plant_name": "Monstera",
            "scientific_name": "Monstera deliciosa",
            "health_status": "Healthy",
            "current_condition": "Leaves look vibrant.",
            "care_plan": {
                "light": "Bright indirect",
                "water": "Weekly",
                "soil": "Well-draining",
                "temperature": "18-27C",
                "humidity": "50-60%"
            },
            "cure_plan": null,
            "common_problems": "Root rot from overwatering."
        }'''
        mock_model = MagicMock()
        mock_model.generate_content.return_value = self._mock_gemini_response(fake_json)
        mock_genai.GenerativeModel.return_value = mock_model

        result = analyze_plant_image(b'fake-image-bytes', 'image/jpeg')

        self.assertEqual(result['plant_name'], 'Monstera')
        self.assertEqual(result['health_status'], 'Healthy')
        self.assertIsNone(result['cure_plan'])
        self.assertIn('light', result['care_plan'])

    @patch('plants.gemini.genai')
    def test_analyze_returns_error_dict_on_invalid_json(self, mock_genai):
        mock_model = MagicMock()
        mock_model.generate_content.return_value = self._mock_gemini_response('not json')
        mock_genai.GenerativeModel.return_value = mock_model

        result = analyze_plant_image(b'fake-image-bytes', 'image/jpeg')

        self.assertIn('error', result)


class AnalyzeViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('analyze')

    def test_get_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'plants/analyze.html')

    @patch('plants.views.analyze_plant_image')
    def test_post_with_image_calls_gemini_and_shows_results(self, mock_analyze):
        mock_analyze.return_value = {
            'plant_name': 'Monstera',
            'scientific_name': 'Monstera deliciosa',
            'health_status': 'Healthy',
            'current_condition': 'Looks great.',
            'care_plan': {
                'light': 'Bright indirect',
                'water': 'Weekly',
                'soil': 'Well-draining',
                'temperature': '18-27C',
                'humidity': '50%',
            },
            'cure_plan': None,
            'common_problems': 'Root rot.',
        }
        image = io.BytesIO(b'fake-image-data')
        image.name = 'plant.jpg'
        response = self.client.post(self.url, {'image': image})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Monstera')
        mock_analyze.assert_called_once()

    def test_post_without_image_shows_error(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please upload an image')
