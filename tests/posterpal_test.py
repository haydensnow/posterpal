import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from posterpal import process_files, load_config, clear_processing_directory
import shutil
import filecmp

def teds_test(self):
    '''
    Check if the Ted files go to the correct location
    '''
    test_config = load_config("./tests/test_config.json")
    clear_processing_directory("tests/shows/Ted Lasso")
    clear_processing_directory("tests/movies/Ted (2012)")
    clear_processing_directory("tests/backup")
    for i in range(10): # Was successful at 50 but reduced for time
        shutil.copy2("tests/zips/Ted Collection set by Tamberlox - 2024-03-20.zip", "test/process/Ted Collection set by Tamberlox - 2024-03-20.zip")
        shutil.copy2("tests/zips/Ted Lasso set by ishalioh - 2024-03-20.zip", "test/process/Ted Lasso set by ishalioh - 2024-03-20.zip")
        
        process_files(test_config)
        
        assert filecmp.cmp("tests/verification/Ted.jpg", "test/movies/Ted (2012)/poster.jpg")
        assert filecmp.cmp("tests/verification/TedLasso.jpg", "test/shows/Ted Lasso/poster.jpg")
        clear_processing_directory("tests/shows/Ted Lasso")
        clear_processing_directory("tests/movies/Ted (2012)")
        clear_processing_directory("tests/backup")