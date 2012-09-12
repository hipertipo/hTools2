# [h] test hWorld

import unittest

class test_hWorld(unittest.TestCase):

    def setUp(self):
        self.hWorld = hWorld()

    def testGetFeedTitle(self):
        #title = "fitnessetesting"
        #self.assertEqual(self.blogger.get_title(), title)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testBlogger))
    return suite

if __name__ == '__main__':
    unittest.main()
