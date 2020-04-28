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

example_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestSmoke(unittest.TestCase):
    # test that the example runs without failing
    def test_smoke(self):
        file_path = os.path.join(example_dir, 'nurse_scheduling.py')

        value = subprocess.check_output(["python", file_path])

        # Check the expected energy
        energy = 0.6
        _, number_etc = str(value).split("Energy  ")
        energy_found, _ = number_etc.split('\\nChecking', 1)
        str2 = 'Checking Hard shift constraint  0.0'
        str3 = 'Checking Hard nurse constraint  0.0'
        str4 = 'Checking Soft nurse constraint  0.6'
        self.assertAlmostEqual(energy, float(energy_found))
        self.assertTrue(str2 in str(value))
        self.assertTrue(str3 in str(value))
        self.assertTrue(str4 in str(value))

if __name__ == '__main__':
    unittest.main()
