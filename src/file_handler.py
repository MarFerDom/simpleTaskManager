import os
import logging
from abc import ABC, abstractmethod
from typing import Iterable, List, Mapping, Optional, Protocol, TextIO
from src.config import _DUMMY_FILE_

__version__ = 0.1

# Set up logger.
logger = logging.getLogger(__name__)

DATA_TYPE = Mapping[str, str]

##############################################
#                                            #
#             PROTOCOL & BASE                #
#                                            #
##############################################

class FileProtocol(Protocol):
    '''
       Protocol for reading and writing from file into a buffer
       with data as a list of json style data per line.
    '''
    def load(self) -> None:
        '''
           load from file to buffer.
        '''
        raise NotImplementedError
    
    def dump(self) -> None:
        '''
           dump from buffer to file.
        '''
        raise NotImplementedError
    
    def buffer(self) -> List[DATA_TYPE]:
        '''
           Returns buffer to share.
        '''
        raise NotImplementedError

    def close(self) -> None:
        '''
           Closes handler.
        '''
        raise NotImplementedError

class FileHandler(ABC):
    '''
       Text buffer for reading writing into file.

       Abstract class for reading and writing into file as a
       list of json style data per line. How each line is 
       stored is implementation dependent.
       Implements simple buffer for loading only if file's
       timestamp changed from last read.
       Static class variable 'handlers' stores existing instances
       of the class.
    '''

    
    # Existing file handlers.
    handlers = dict()
    
    def __new__(cls, filename:str = _DUMMY_FILE_,
                *args, **kwargs):
        '''
           Guarantees only one instance of the class is created per filename.
        '''

        if filename not in FileHandler.handlers:
            # Creates new object.
            FileHandler.handlers[filename] = \
                super(FileHandler, cls).__new__(cls)
            # Resets for initialization.
            FileHandler.handlers[filename]._initialized = False
        return FileHandler.handlers[filename]
    
    def close(self):
        '''
           Removes handler from handler list and clears the buffer.
        '''

        FileHandler.handlers.pop(self._file)
        self._buffer.clear()

    def __init__(self, filename:str = _DUMMY_FILE_, labels:List[str] = [],
                 default_content:str = '', *args, **kwargs):
        super(FileHandler, self).__init__(*args, **kwargs)
        '''
           Initialize:
           - path of file handle,
           - labels for json style attributes
           - default content when creating a file.
        '''

        # Skip initialization for existing file handlers.
        if self._initialized: return

        self._file = filename
        self._labels = labels
        self._default_content = default_content

        # - buffer for read data,
        # - timestamp for reading only if file changed.
        self._buffer: List[DATA_TYPE] = list()
        self._timestamp: Optional[float] = None

        # If file exists, return.
        if os.path.exists(self._file): return

        # If not, write default content.
        # Tries to write/create file 3 times beflre raising the Error.
        tries = 3
        for i in range(tries):
            try:
                with open(self._file, "w") as default_file:
                    default_file.write(self._default_content)
                    return
            except Exception as e:
                if i+1 == tries:
                    self.close()
                    raise e

        self._initialized = True

    def time_stamp_alt(self):
        '''
           Checks if timestamp changed since last load.
        '''

        old_timestamp, self._timestamp = self._timestamp, os.stat(self._file).st_mtime
        return old_timestamp is None or self._timestamp != old_timestamp
    
    def dump(self) -> None:
        '''
           dump available input in file.
        '''

        if not self._buffer: return
        with open(self._file, 'w') as f:
            logger.info(f'File {self._file} open for writing by {self.__class__}')
            self._implementation_dump(f)

    def load(self) -> None:
        '''
           load file if changed since last load.
        '''
        
        if self.time_stamp_alt():
            with open(self._file, 'r') as f:
                logger.info(f'File {self._file} open for reading by {self.__class__}')
                self._buffer.clear()
                self._buffer.extend(self._implementation_load(f))
    
    @abstractmethod
    def _implementation_dump(self, textfile:TextIO) -> None:
        '''
           Implement on derived classes
        '''
        raise NotImplementedError
    
    @abstractmethod
    def _implementation_load(self, textfile:TextIO) -> List[DATA_TYPE]:
        '''
           Implement on derived classes
        '''
        raise NotImplementedError
    
    @property
    def buffer(self):
        return self._buffer
    
##############################################
#                                            #
#             IMPLEMENTATIONS                #
#                                            #
##############################################


class SCSVFileHandler(FileHandler):
    '''
       Class that deals with a semicolon separated values file

        - Initialize with filename and default content,
        - load and dump lists of DATA_TYPE,
        - if '_labels' is not defined, apply numeric labels.
    '''
    def __init__(self, *args, **kwargs):
        super(SCSVFileHandler, self).__init__(*args, **kwargs)
        
    def _build_line(self, dic:DATA_TYPE) -> str:
        '''
           Build a line in SCSV format with handler's label order.
        '''

        if len(self._labels):
            line = [dic[k] for k in self._labels if k in dic]
            pad_size = len(self._labels) - len(line)
        else:
            line = list(dic.values())
            pad_size = 0
        return ';'.join(line + ['']*pad_size)

    def _implementation_dump(self, file:TextIO) -> None:
        '''
           Implementation of dump for SCSV file.
        '''

        if not len(self.buffer): return
        file.write(self._build_line(self._buffer[0]))
        for line in self._buffer[1:]:
            file.write('\n'+self._build_line(line))
    
    def _implementation_load(self, file:TextIO) -> List[DATA_TYPE]:
        '''
           Implementation of load for SCSV file.
        '''

        # Use set labels if defined:
        # - Entries will be limited by number of labels.
        if len(self._labels):
            return  list(map(
                lambda line: {k:v for k,v in \
                              zip(self._labels, line.rstrip('\n').split(';'))},
                file.readlines()
                ))
        # Else use numeric labels:
        # - Entries will not be limited.
        return list(map(
            lambda line: {str(i):v for i,v in enumerate(line.rstrip('\n').split(';'))},
            file.readlines()
            ))
        


class ReportFileHandler(FileHandler):
    '''
       Class that deals with a report file.

       To read as presentable text just print it directly.
    '''
    def __init__(self, pre_header: str = '', *args, **kwargs):
        super(ReportFileHandler, self).__init__(*args, **kwargs)

        # Build equal spacing header.
        self._spacing = max((len(label) for label in kwargs['labels'])) + 4
        self.header = '\t'.join(
            (label.ljust(self._spacing) for label in kwargs['labels']))
        self.space_line = '\n'+'-'*len(self.header)

        # Set initial value for pre header text.
        self._pre_header = pre_header

    def _build_line(self, line:DATA_TYPE) -> Iterable[str]:
        '''
           Build a line in report format with handler's label order.
        '''

        return (line.get(label, '').ljust(self._spacing) for label in self._labels)

    def _implementation_dump(self, file:TextIO) -> None:
        '''
           Writes pre header (if set), header, and a line in report format
           for each list of data dictionaries, between to spacing lines.
        '''

        # If has pre header write in file.
        if len(self._pre_header): file.write(self._pre_header + '\n')
        # Write header and line spacing.
        file.write(self.header+self.space_line)
                        
        # For each line of data write in report format.
        for line in self.buffer:
            file.write('\n'+'\t'.join(self._build_line(line)))
        # Write a line spacing.
        file.write(self.space_line)
    
    def _implementation_load(self, file:TextIO) -> List[DATA_TYPE]:
        """
           Return a list of dictionaries for each
           line that is not header or spacing.
        """

        # Get number of lines to skip:
        # - Number of pre_header lines plus header and spacing line.
        skip = len(self._pre_header.split('\n'))+2 if len(self._pre_header) else 2
        # Line is split by tabs and white spaces removed.
        return [{k:v.strip() for k,v in zip(self._labels, line.split('\t'))}
                # For each line ignoring the first 'skip' and the last.
                for line in file.readlines()[skip:]]
    
    def set_pre_header(self, pre_header:str = '') -> None:
        '''
           Set pre header text.
        '''

        self._pre_header = pre_header

    def __str__(self) -> str:
        '''
           Read file as text to print.
        '''

        with open(self._file, 'r') as f:
            return f.read()


if __name__ == '__main__':

    handler = SCSVFileHandler()
    print(list(FileHandler.handlers.keys()))
    handler.close()
    print(list(FileHandler.handlers.keys()))