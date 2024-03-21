import unittest
from posterpal import process_files, load_config, clear_processing_directory
import shutil
import filecmp

class TestProcess(unittest.TestCase):
    def test_teds(self):
        '''
        Check if the Ted files go to the correct location
        '''
        test_config = load_config("./test/test_config.json")
        clear_processing_directory("test/shows/Ted Lasso")
        clear_processing_directory("test/movies/Ted (2012)")
        clear_processing_directory("test/backup")
        for i in range(10): # Was successful at 50 but reduced for time
            shutil.copy2("test/zips/Ted Collection set by Tamberlox - 2024-03-20.zip", "test/process/Ted Collection set by Tamberlox - 2024-03-20.zip")
            shutil.copy2("test/zips/Ted Lasso set by ishalioh - 2024-03-20.zip", "test/process/Ted Lasso set by ishalioh - 2024-03-20.zip")
            process_files(test_config)
            
            self.assertTrue(filecmp.cmp("test/verification/Ted.jpg", "test/movies/Ted (2012)/poster.jpg"), "Ted failed")
            self.assertTrue(filecmp.cmp("test/verification/TedLasso.jpg", "test/shows/Ted Lasso/poster.jpg"), "Ted Lasso failed");
            clear_processing_directory("test/shows/Ted Lasso")
            clear_processing_directory("test/movies/Ted (2012)")
            clear_processing_directory("test/backup")


if __name__ == "__main__":
    unittest.main()