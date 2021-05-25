# Copyright 2020 D-Wave Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import subprocess
import unittest
import sys

example_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class IntegrationTests(unittest.TestCase):
    @unittest.skipIf(os.getenv('SKIP_INT_TESTS'), "Skipping integration test.")    
    def test_schedule(self):
        file_path = os.path.join(example_dir, 'nurse_scheduling.py')

        output = str(subprocess.check_output([sys.executable, file_path]))

        # Check constraints
        str2 = 'Hard shift constraint: Satisfied'
        str3 = 'Hard nurse constraint: Satisfied'

        self.assertIn(str2, output)
        self.assertIn(str3, output)

if __name__ == '__main__':
    unittest.main()
