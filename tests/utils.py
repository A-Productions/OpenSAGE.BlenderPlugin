# <pep8 compliant>
# Written by Stephan Vedder and Michael Schnabel

import unittest
import inspect
import os
import shutil
import sys
import tempfile
import bpy

import addon_utils


def almost_equal(self, x, y, threshold=0.0001):
    self.assertTrue(abs(x - y) < threshold)


class ImportWrapper:
    def __init__(self, filepath):
        self.filepath = filepath
        self.report = print


class W3dTestCase(unittest.TestCase):
    __save_test_data = '--save-test-data' in sys.argv
    __tmp_base = os.path.join(tempfile.gettempdir(), 'io_mesh_w3d-tests')
    __tmp = __tmp_base + '/out'
    _reports = []

    @classmethod
    def relpath(cls, path=None):
        result = os.path.dirname(inspect.getfile(cls))
        if path is not None:
            result = os.path.join(result, path)
        return result

    @classmethod
    def outpath(cls, path=''):
        if not os.path.exists(cls.__tmp):
            os.makedirs(cls.__tmp)
        return os.path.join(cls.__tmp, path)

    def loadBlend(self, blend_file):
        bpy.ops.wm.open_mainfile(filepath=self.relpath(blend_file))

    def setUp(self):
        bpy.ops.wm.read_homefile(use_empty=True)
        addon_utils.enable('io_mesh_w3d', default_set=True)

    def tearDown(self):
        if os.path.exists(self.__tmp):
            if self.__save_test_data:
                bpy.ops.wm.save_mainfile(
                    filepath=os.path.join(self.__tmp, 'result.blend'))
                new_path = os.path.join(
                    self.__tmp_base,
                    self.__class__.__name__,
                    self._testMethodName)
                os.renames(self.__tmp, new_path)
            else:
                shutil.rmtree(self.__tmp)
        addon_utils.disable('io_mesh_w3d')

    def assertObjectsExist(self, obj_list):
        for obj_name in obj_list:
            self.assertIsNotNone(bpy.data.objects.get(
                obj_name), "No object named: " + obj_name)
