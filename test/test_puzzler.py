import unittest
import sys
sys.path.append('./../src/')
import puzzler


class Test_Puzzler(unittest.TestCase):
    def test_puzzler_consistency(self):
        '''
            Check the puzzler for consistency
        '''
        em = 'random.email@organization.name.org'
        pswd = 'abcd' # stupidly weak password

        self.assertEqual(puzzler.puzzle_gen(em,pswd),puzzler.puzzle_gen(em,pswd))

    def test_time_taken(self):
        '''
            Tests the time complexity of puzzle generation ( optimally independent of size of input (const))
        '''

        em = 'random.email@organization.name.org'
        pswd = 'abcd' # stupidly weak password

        for _ in range(100000):
            self.assertEqual(puzzler.puzzle_gen(em,pswd),puzzler.puzzle_gen(em,pswd))

if __name__ == '__main__':
    unittest.main()