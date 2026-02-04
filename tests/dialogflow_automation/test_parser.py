import unittest
import json
import os
import shutil
import tempfile
from dialogflow_automation.core.parser import ConfigParser

class TestConfigParser(unittest.TestCase):
    def setUp(self):
        # Cria diretório temporário para testes
        self.test_dir = tempfile.mkdtemp()
        self.parser = ConfigParser(self.test_dir)

    def tearDown(self):
        # Remove diretório temporário após cada teste
        shutil.rmtree(self.test_dir)

    def create_dummy_json(self, filename, content):
        with open(os.path.join(self.test_dir, filename), 'w') as f:
            json.dump(content, f)

    def test_load_valid_intents(self):
        valid_data = [
            {
                "display_name": "test_intent",
                "training_phrases": ["phrase 1", "phrase 2"],
                "messages": ["response 1"]
            }
        ]
        self.create_dummy_json("intents.json", valid_data)
        
        intents = self.parser.load_intents()
        self.assertEqual(len(intents), 1)
        self.assertEqual(intents[0]["display_name"], "test_intent")

    def test_missing_required_field(self):
        invalid_data = [
            {
                "training_phrases": ["phrase 1"],
                "messages": ["response 1"]
            }
        ]
        self.create_dummy_json("intents.json", invalid_data)
        
        with self.assertRaises(ValueError) as cm:
            self.parser.load_intents()
        self.assertIn("Campo obrigatório 'display_name' ausente", str(cm.exception))

    def test_invalid_field_type(self):
        invalid_data = [
            {
                "display_name": "test_intent",
                "training_phrases": "not a list",
                "messages": ["response 1"]
            }
        ]
        self.create_dummy_json("intents.json", invalid_data)
        
        with self.assertRaises(ValueError) as cm:
            self.parser.load_intents()
        self.assertIn("deve ser do tipo list", str(cm.exception))

    def test_invalid_list_content(self):
        invalid_data = [
            {
                "display_name": "test_intent",
                "training_phrases": [123, "phrase 2"],
                "messages": ["response 1"]
            }
        ]
        self.create_dummy_json("intents.json", invalid_data)
        
        with self.assertRaises(ValueError) as cm:
            self.parser.load_intents()
        self.assertIn("deve conter apenas strings", str(cm.exception))

    def test_parameter_validation(self):
        invalid_data = [
            {
                "display_name": "test_intent",
                "training_phrases": [],
                "messages": [],
                "parameters": [
                    {
                        "display_name": "param1",
                        # "entity_type_display_name" missing
                        "mandatory": True
                    }
                ]
            }
        ]
        self.create_dummy_json("intents.json", invalid_data)
        
        with self.assertRaises(ValueError) as cm:
            self.parser.load_intents()
        self.assertIn("Campo 'entity_type_display_name' ausente", str(cm.exception))

if __name__ == '__main__':
    unittest.main()
