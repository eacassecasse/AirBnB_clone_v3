#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""


class TestDBStorageCountGet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the storage engine before any tests are run
        storage_type = os.getenv('HBNB_TYPE_STORAGE')
        if storage_type == 'db':
            from models.engine.db_storage import DBStorage
            cls.storage = DBStorage()
        else:
            from models.engine.file_storage import FileStorage
            cls.storage = FileStorage()
    
    def setUp(self):
        """
        Creating storage and objects 
        """
        self.state1 = State(id="c1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890", name="Nebraska")
        self.state2 = State(id="4f3a2b1c-0d9e-8f7g-6h5i-4j3k2l1m0n9o", name="Georgia")
        models.storage.new(self.state1)
        models.storage.new(self.state2)
        models.storage.save()

    def test_get_existing_object(self):
        """ Testing if the get method gets an existing object """
        result = models.storage.get(State, "c1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890")
        self.assertEqual(result, self.state1)

    def test_get_non_existing_object(self):
        """ Testing if the get method gets an non-existing object """

        result = models.storage.get(State, "f4e3d2c1-b5a6-7980-c1d2-e3f4g5h6i7j8")
        self.assertIsNone(result)

    def test_get_with_invalid_class(self):
        """ Testing if the get method gets with an invalid class """
        result = models.storage.get("InvalidClass", "c1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890")
        self.assertIsNone(result)

    def test_get_with_valid_class_no_objects(self):
        """ Testing if the get method gets with a valid class but, 
        non-existing object """
        result = models.storage.get(State, "f4e3d2c1-b5a6-7980-c1d2-e3f4g5h6i7j8")
        self.assertIsNone(result)

    def test_count_all_objects(self):
        """ Testing count for all object """
        result = models.storage.count()
        self.assertEqual(result, 2)

    def test_count_specific_class_objects(self):
        """ Testing count with a specific class """
        result = models.storage.count(State)
        self.assertEqual(result, 2)

    def test_count_with_invalid_class(self):
        """ Testing count with an invalid class """
        result = models.storage.count("InvalidClass")
        self.assertEqual(result, 0)

    def test_count_with_valid_class_no_objects(self):
        """ Testing count with a class without objects """
        result = models.storage.count(City)
        self.assertEqual(result, 0)

    def tearDown(self):
        """ Clean up for the test objects """
        models.storage.delete(self.state1)
        models.storage.delete(self.state2)
        models.storage.save()

if __name__ == '__main__':
    unittest.main()

