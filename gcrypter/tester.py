# ******************************************************************************
#  (c) 2019-2021 Nurul-GC.                                                     *
# ******************************************************************************

import unittest
from datetime import datetime

from gcrypter import db


class MyTestCase(unittest.TestCase):
    def test_atualizarcreated(self):
        self.assertTrue(db.G6RDB().atualizar_created(_nome='Nurul', _created=datetime.today()))

    def test_atualizarlastlogin(self):
        self.assertTrue(db.G6RDB().atualizar_lastlogin(_nome='Nurul', _last_login=datetime.today()))


if __name__ == '__main__':
    unittest.main()
