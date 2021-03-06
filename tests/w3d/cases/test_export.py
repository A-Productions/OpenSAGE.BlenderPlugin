# <pep8 compliant>
# Written by Stephan Vedder and Michael Schnabel

import bpy
import os.path
from tests.utils import *
from io_mesh_w3d.w3d.export_w3d import save
from io_mesh_w3d.import_utils import *

from tests.w3d.helpers.mesh import *
from tests.w3d.helpers.hlod import *
from tests.w3d.helpers.hierarchy import *


class TestExport(TestCase):
    def test_unsupported_export_mode(self):
        export_settings = {}
        export_settings['w3d_mode'] = "NON_EXISTING"

        self.assertEqual({'CANCELLED'}, save(self, export_settings))

    def test_no_file_created_if_MODE_is_M_and_no_meshes(self):
        export_settings = {}
        export_settings['w3d_mode'] = "M"

        file_path = self.outpath() + "output_skn.w3d"
        context = ImportWrapper(file_path)

        self.assertEqual({'CANCELLED'}, save(context, export_settings))

        self.assertFalse(os.path.exists(file_path))

    def test_no_hlod_is_written_if_M_and_less_than_2_sub_objects(self):
        export_settings = {}
        export_settings['w3d_mode'] = "M"
        export_settings['w3d_compression'] = "U"

        meshes = [get_mesh()]
        create_data(self, meshes)

        file_path = self.outpath() + "output_skn.w3d"
        context = ImportWrapper(file_path)

        self.assertEqual({'FINISHED'}, save(context, export_settings))

        file = open(file_path, "rb")
        filesize = os.path.getsize(file_path)
        while file.tell() < filesize:
            (chunk_type, chunk_size, chunk_end) = read_chunk_head(file)

            self.assertNotEqual(W3D_CHUNK_HLOD, chunk_type)
            skip_unknown_chunk(self, file, chunk_type, chunk_size)

        file.close()

    def test_no_file_created_if_MODE_is_HAM_and_no_meshes(self):
        export_settings = {}
        export_settings['w3d_mode'] = "HAM"

        file_path = self.outpath() + "output_skn.w3d"
        context = ImportWrapper(file_path)

        self.assertEqual({'CANCELLED'}, save(context, export_settings))

        self.assertFalse(os.path.exists(file_path))

    def test_no_hierarchy_is_written_if_HAM_and_less_than_2_pivots(self):
        export_settings = {}
        export_settings['w3d_mode'] = "HAM"
        export_settings['w3d_compression'] = "U"

        meshes = [get_mesh()]
        create_data(self, meshes)

        file_path = self.outpath() + "output_skn.w3d"
        context = ImportWrapper(file_path)

        self.assertEqual({'FINISHED'}, save(context, export_settings))

        file = open(file_path, "rb")
        filesize = os.path.getsize(file_path)
        while file.tell() < filesize:
            (chunk_type, chunk_size, chunk_end) = read_chunk_head(file)

            self.assertNotEqual(W3D_CHUNK_HIERARCHY, chunk_type)
            skip_unknown_chunk(self, file, chunk_type, chunk_size)

        file.close()

    def test_no_hlod_is_written_if_HAM_and_less_than_2_sub_objects(self):
        export_settings = {}
        export_settings['w3d_mode'] = "HAM"
        export_settings['w3d_compression'] = "U"

        meshes = [get_mesh()]
        create_data(self, meshes)

        file_path = self.outpath() + "output_skn.w3d"
        context = ImportWrapper(file_path)

        self.assertEqual({'FINISHED'}, save(context, export_settings))

        file = open(file_path, "rb")
        filesize = os.path.getsize(file_path)
        while file.tell() < filesize:
            (chunk_type, chunk_size, chunk_end) = read_chunk_head(file)

            self.assertNotEqual(W3D_CHUNK_HLOD, chunk_type)
            skip_unknown_chunk(self, file, chunk_type, chunk_size)

        file.close()

    def test_no_file_created_if_MODE_is_H_and_less_than_2_pivots(self):
        export_settings = {}
        export_settings['w3d_mode'] = "H"

        file_path = self.outpath() + "output_skl.w3d"
        context = ImportWrapper(file_path)

        self.assertEqual({'CANCELLED'}, save(context, export_settings))

        self.assertFalse(os.path.exists(file_path))

    def test_no_file_created_if_MODE_is_A_and_U_no_animation_channels(self):
        export_settings = {}
        export_settings['w3d_mode'] = "A"
        export_settings['w3d_compression'] = "U"

        file_path = self.outpath() + "output_ani.w3d"
        context = ImportWrapper(file_path)

        self.assertEqual({'CANCELLED'}, save(context, export_settings))

        self.assertFalse(os.path.exists(file_path))

    def test_no_file_created_if_MODE_is_A_and_TC_no_animation_channels(self):
        export_settings = {}
        export_settings['w3d_mode'] = "A"
        export_settings['w3d_compression'] = "TC"

        file_path = self.outpath() + "output_ani.w3d"
        context = ImportWrapper(file_path)

        self.assertEqual({'CANCELLED'}, save(context, export_settings))

        self.assertFalse(os.path.exists(file_path))