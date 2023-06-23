import unittest
from unittest import mock
from src import file_handler

PATCH_OPEN = "src.file_handler.open"
PATCH_PATH = "src.file_handler.os.path.exists"
PATCH_STAT = "src.file_handler.os.stat"

mock_path = mock.MagicMock(return_value=True)
mock_open = mock.MagicMock()
mock_file = mock.MagicMock()
mock_stat = mock.MagicMock()
mock_timestamp = mock.MagicMock()

mock_stat.return_value = mock_timestamp
mock_timestamp.st_mtime = 1
mock_file.__enter__.return_value = mock_file
##############################################################################
##############################################
#                                            #
#        file_handler.SCSVHandler            #
#                                            #
##############################################

@mock.patch(PATCH_STAT, mock_stat)
@mock.patch(PATCH_PATH, mock_path)
@mock.patch(PATCH_OPEN, mock_open)
class TestSCSVFileHandler(unittest.TestCase):
##############################################
#                                            #
#             INITIALIZATION                 #
#                                            #
##############################################
   def setUp(self) -> None:
      mock_open.reset_mock()
      mock_open.return_value = mock_file
      return super().setUp()
   
   def tearDown(self) -> None:

      return super().tearDown()
   
   def test_handler_is_singelton(self):
      '''
         Test if handler is singelton.
      '''

      handler1 = file_handler.SCSVFileHandler()
      handler2 = file_handler.SCSVFileHandler()
      self.assertIs(handler1, handler2, 'Created two handlers for same file')
      handler1.close()

   def test_handler_is_singelton_per_file(self):
      '''
         Test if handler is singelton per filename.
      '''

      handler1 = file_handler.SCSVFileHandler()
      handler2 = file_handler.SCSVFileHandler(filename='another')
      self.assertIsNot(handler1, handler2, 'Did not create handler for second file')
      handler1.close()
      handler2.close()

   def test_not_create_existing_file(self):
      '''
         Test if tries to create file that already exists.
      '''

      file_handler.SCSVFileHandler().close()

      self.assertFalse(mock_open.called,
                        "Tried to create file that already existed")
   

   def test_create_fail_open(self):
      '''
         Test if tries to create file 3 times with
         default filename is exception raised.
      '''

      mock_path.return_value = False
      mock_open.side_effect = Exception("Can't open file!")

      # Asserts called three time with DUMMY raising an exception.
      self.assertRaises(Exception, file_handler.SCSVFileHandler)
      self.assertEqual(mock_open.call_count, 3)
      mock_open.assert_called_with(file_handler._DUMMY_FILE_, 'w')
      file_handler.FileHandler.handlers.clear()

      mock_open.side_effect = None
      mock_path.return_value = True

   def test_create_filename_content(self):
      '''
         Test if creates with passed argument filename and content.
      '''

      mock_path.return_value = False

      file_handler.SCSVFileHandler(filename='FILENAME',
                                 default_content='CONTENT').close()
      
      mock_open.assert_called_with('FILENAME', 'w')
      mock_file.write.assert_called_with('CONTENT')

      mock_path.return_value = True


##############################################
#                                            #
#          READING AND WRITING               #
#                                            #
##############################################


   def test_write_file(self):
      '''
         Test if writes lines to a file.
      '''

      f_handler = file_handler.SCSVFileHandler(labels=['1', '2', '3'])
      buffer = f_handler.buffer
      
      # Write one line
      buffer.extend([
         {'1':'semi-collon', '3':'values', '':'banana', '2':'separated'}])
      f_handler.dump()

      mock_file.write.assert_called_with('semi-collon;separated;values')

      # Write two lines
      buffer.extend([
         {'2':'what will happen', '5':'with less labels'}])
      f_handler.dump()

      mock_file.write.assert_called_with('\nwhat will happen;;')

      f_handler.close()

   def test_write_no_label(self):
      '''
         Test if writes lines to a file without label.
      '''

      f_handler = file_handler.SCSVFileHandler()
      buffer = f_handler.buffer
      # Write one line
      buffer.extend([
         {'1':'semi-collon', '3':'values', '':'banana', '2':'separated'}])
      f_handler.dump()

      mock_file.write.assert_called_with('semi-collon;values;banana;separated')

      f_handler.close()


   def test_read_file(self):
      '''
         Test if reads lines from a file.
      '''

      mock_file.readlines.return_value = ['what;ever;will;be;will;be',
                                          'the;future;is;ours;to;see']
      f_handler = file_handler.SCSVFileHandler(labels=['1', '2', '3'])
      f_handler.load()

      self.assertEqual(f_handler.buffer,
                        [{'1':'what','2':'ever', '3':'will'},
                        {'1':'the','2':'future', '3':'is'}])
      
      mock_file.readlines.return_value = None
      f_handler.close()
      

   def test_read_buffer(self):
      '''
         Test if reads lines from buffer on second read.
      '''

      f_handler = file_handler.SCSVFileHandler()
      mock_imp_read = mock.MagicMock()
      with mock.patch.object(f_handler,
                              '_implementation_load') as mock_imp_read:
         f_handler.load()
         f_handler.load()
         f_handler.load()

      self.assertEqual(mock_imp_read.call_count, 1)
      f_handler.close()
        


##############################################################################
##############################################
#                                            #
#      file_handler.ReportFileHandler        #
#                                            #
##############################################

@mock.patch(PATCH_STAT, mock_stat)
@mock.patch(PATCH_PATH, mock_path)
@mock.patch(PATCH_OPEN, mock_open)
class TestReportFileHandler(unittest.TestCase):
##############################################
#                                            #
#             INITIALIZATION                 #
#                                            #
##############################################

   def setUp(self) -> None:
      mock_open.reset_mock()
      mock_open.return_value = mock_file
      mock_file.reset_mock()
      return super().setUp()
   
   def tearDown(self) -> None:
      file_handler.FileHandler.handlers.clear()
      return super().tearDown()
   
##############################################
#                                            #
#          READING AND WRITING               #
#                                            #
##############################################

   def test_write_report_file(self):
      '''
         Test if writes lines to a file.
      '''

      handler = file_handler.ReportFileHandler(
          labels=[f'Label {i}' for i in range(7)],
          pre_header='PRE HEADER TEXT')
      #mock_path.return_value = True
      mock_file.__enter__.return_value = mock_file
      mock_open.return_value = mock_file
      buffer = handler.buffer

      # Insert on buffer a single line with 'entry' for each label.
      buffer.extend([
         dict.fromkeys([f'Label {i}' for i in range(7)], 'entry')])
      handler.dump()
      
      # Expected output
      expected = ['PRE HEADER TEXT\n']
      header = '\t'.join([f'Label {i}    ' for i in range(7)])
      sep_line = '\n'+'-'*len(header)
      expected.append(header+sep_line)
      expected.append('\n'+'\t'.join(['entry'.ljust(11)]*7))
      expected.append(sep_line)

      for call_read, arg in zip(mock_file.write.mock_calls, expected):
          self.assertEqual(call_read.args, (arg,))

      mock_file.write.mock_calls.clear()

      # Insert on buffer another line with 'another' for each label.
      buffer.extend([
         dict.fromkeys([f'Label {i}' for i in range(7)], 'another')])
      handler.dump()

      handler.close()

      # Expected output
      expected.pop()
      expected.append('\n'+'\t'.join(['another'.ljust(11)]*7))
      expected.append(sep_line)

      for call_read, arg in zip(mock_file.write.mock_calls, expected):
          self.assertEqual(call_read.args, (arg,))


   def test_set_pre_header(self):
      '''
         Test changing pre header.
      '''

      handler = file_handler.ReportFileHandler(
          labels=[f'Label {i}' for i in range(7)],
          pre_header='PRE HEADER TEXT')
      
      mock_file.__enter__.return_value = mock_file
      mock_open.return_value = mock_file
      buffer = handler.buffer

      # Insert on buffer a single line with 'entry' for each label.
      buffer.extend([
         dict.fromkeys([f'Label {i}' for i in range(7)], 'entry')])
      handler.set_pre_header('CHANGE PRE HEADER')
      handler.dump()
      
      handler.close()

      # Expected output
      expected = ['CHANGE PRE HEADER\n']
      header = '\t'.join([f'Label {i}    ' for i in range(7)])
      sep_line = '\n'+'-'*len(header)
      expected.append(header+sep_line)
      expected.append('\n'+'\t'.join(['entry'.ljust(11)]*7))
      expected.append(sep_line)

      for call_read, arg in zip(mock_file.write.mock_calls, expected):
          self.assertEqual(call_read.args, (arg,))


   def test_read_report_file(self):
      '''
         Test if reads lines from a file.
      '''

      handler = file_handler.ReportFileHandler(
          labels=[f'Label {i}' for i in range(7)],
          pre_header='PRE HEADER TEXT')
      
      #mock_path.return_value = True
      mock_file.__enter__.return_value = mock_file
      mock_file.read = mock.MagicMock()
      mock_file.read.side_effect = ['TEST STRING']

      self.assertEqual(str(handler), 'TEST STRING')
      handler.close()

      
if __name__=='__main__':
    unittest.main()
