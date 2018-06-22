from diskspace import *
import unittest
from unittest.mock import MagicMock

class TestSubprocessCheckOutputMethod(unittest.TestCase):
    def setUp(self):
        self.mock = MagicMock()
        self.mock.command = '    du -d 1 /home/MyVideos    '
        self.mock.command2 = 'du -d 1 /home/MyVideos'
        self.mock.command3 = '4708068	/home/MyVideos'
        self.subprocess_check_output = MagicMock()

    def test_strStrip(self):
        self.assertEqual(self.mock.command.strip(), self.mock.command2)

    def test_strSplit(self):
        self.assertEqual(self.mock.command.strip().split(' '), ['du', '-d', '1', '/home/MyVideos'])
        with self.assertRaises(ValueError):
            self.mock.command.split('')

    def test_function_call(self):
        self.subprocess_check_output(self.mock.command2)
        self.assertIsInstance(self.mock.command2, str)
        self.subprocess_check_output.assert_called_with(self.mock.command2)
        self.assertEqual(str(self.subprocess_check_output.mock_calls), '[call('+ '\'du -d 1 /home/MyVideos\''+')]')

    def test_function_return(self):
        self.subprocess_check_output = MagicMock(return_value = self.mock.command3)
        self.subprocess_check_output(self.mock.command2)
        self.assertEqual(self.subprocess_check_output.return_value, self.mock.command3)

suite = unittest.TestLoader().loadTestsFromTestCase(TestSubprocessCheckOutputMethod)
unittest.TextTestRunner(verbosity=2).run(suite)

class TestBytesToReadableMethod(unittest.TestCase):
    def setUp(self):
        self.mock = MagicMock()
        self.mock.block = 48908
        self.mock.byts = 111398912
        self.mock.labels = ['B', 'Kb', 'Mb', 'Gb', 'Tb']
        self.mock.count = 2
        self.bytes_to_readable = MagicMock()
        self.mock.function_return = '106.24Mb'

    def test_round(self):
        self.assertEqual(round(self.mock.byts/(1024.0**self.mock.count), 2), 106.24)

    def test_format(self):
        self.assertEqual('{:.2f}{}'.format(round(self.mock.byts/(1024.0**self.mock.count), 2),
                                            self.mock.labels[self.mock.count]), self.mock.function_return)

    def test_function_call(self):
        self.bytes_to_readable(self.mock.block)
        self.assertIsInstance(self.mock.block, int)
        self.bytes_to_readable.assert_called_with(self.mock.block)
        self.assertEqual(str(self.bytes_to_readable.mock_calls), '[call('+ str(self.mock.block)+')]')

    def test_function_return(self):
        self.mock.function_return = self.bytes_to_readable(self.mock.block)
        self.bytes_to_readable = MagicMock(return_value = self.mock.function_return)
        self.bytes_to_readable(self.mock.block)
        self.assertEqual(self.bytes_to_readable.return_value, self.mock.function_return)

suite = unittest.TestLoader().loadTestsFromTestCase(TestBytesToReadableMethod)
unittest.TextTestRunner(verbosity=2).run(suite)

class TestDiskspacePrintTreeMethod(unittest.TestCase):
    def setUp(self):
        self.mock = MagicMock()
        self.mock.file_tree = {'/home/MyVideos/test': {'print_size': '106.24Mb', 'children': [],
                                'size': 217576}, '/home/MyVideos': {'print_size': '2.24Gb',
                                'children': ['/home/MyVideos/test'], 'size': 4708068}}
        self.mock.file_tree_node = {'print_size': '2.24Gb', 'children': ['/home/MyVideos/test'], 'size': 4708068}
        self.mock.path = '/home/MyVideos'
        self.mock.largest_size = 8
        self.mock.total_size = 4708068
        self.mock.depth = 0
        self.mock.percentage = 100
        self.mock.function_return = None
        self.print_tree = MagicMock()

    def test_convertion(self):
        self.assertEqual(float(self.mock.total_size), 4708068.0)
        self.assertEqual(int(self.mock.file_tree_node['size'] / float(self.mock.total_size) * 100), 100)

    def test_format(self):
        self.assertEqual('{:>{}s} {:>4d}%  '.format(self.mock.file_tree_node['print_size'], self.mock.largest_size, self.mock.percentage),'  2.24Gb  100%  ')
        self.assertEqual('{}{}'.format('   '*self.mock.depth, os.path.basename(self.mock.path)),'MyVideos')

    def test_function_call(self):
        self.print_tree(self.mock.file_tree, self.mock.file_tree_node, self.mock.path, self.mock.largest_size,
                                    self.mock.total_size, self.mock.depth)
        self.assertIsInstance(self.mock.file_tree, dict)
        self.assertIsInstance(self.mock.file_tree_node, dict)
        self.assertIsInstance(self.mock.path, str)
        self.assertIsInstance(self.mock.largest_size, int)
        self.assertIsInstance(self.mock.total_size, int)
        self.assertIsInstance(self.mock.depth, int)
        self.print_tree.assert_called_with(self.mock.file_tree, self.mock.file_tree_node, self.mock.path, self.mock.largest_size,
                                    self.mock.total_size, self.mock.depth)

    def test_function_return(self):
        self.print_tree = MagicMock(return_value = self.mock.function_return)
        self.print_tree()
        self.assertEqual(self.print_tree.return_value, self.mock.function_return)

suite = unittest.TestLoader().loadTestsFromTestCase(TestDiskspacePrintTreeMethod)
unittest.TextTestRunner(verbosity=2).run(suite)

class TestDiskspaceShowSpaceListMethod(unittest.TestCase):
    def setUp(self):
        self.mock = MagicMock()
        self.mock.directory =  '/home/MyVideos/'
        self.mock.depth = 1
        self.mock.order = True
        self.mock.line = ('4708068', '/home/MyVideos')
        self.mock.function_return = None
        self.show_space_list = MagicMock()

    def test_convertion(self):
        self.assertEqual(int(self.mock.line[0]), 4708068)

    def test_format(self):
        self.assertEqual('-d {} '.format(self.mock.depth),'-d 1 ')

    def test_function_call(self):
        self.show_space_list(self.mock.directory, self.mock.depth, self.mock.order)
        self.assertIsInstance(self.mock.directory, str)
        self.assertIsInstance(self.mock.depth, int)
        self.assertIsInstance(self.mock.order, bool)
        self.show_space_list.assert_called_with(self.mock.directory, self.mock.depth, self.mock.order)

    def test_function_return(self):
        self.show_space_list = MagicMock(return_value = self.mock.function_return)
        self.show_space_list()
        self.assertEqual(self.show_space_list.return_value, self.mock.function_return)

suite = unittest.TestLoader().loadTestsFromTestCase(TestDiskspaceShowSpaceListMethod)
unittest.TextTestRunner(verbosity=2).run(suite)
