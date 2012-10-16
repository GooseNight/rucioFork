# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Vincent Garonne, <vincent.garonne@cern.ch>, 2012
# - Mario Lassnig, <mario.lassnig@cern.ch>, 2012
# - Angelos Molfetas, <angelos.molfetas@cern.ch>, 2012
# - Thomas Beermann, <thomas.beermann@cern.ch>, 2012

from os import remove

import nose.tools
import re

from rucio import version
from rucio.db.session import build_database, destroy_database, create_root_account
from rucio.tests.common import execute


class TestBinRucio():

    def setUp(self):
        build_database(echo=False)
        create_root_account()
        try:
            remove('/tmp/.rucio_root/auth_token_root')
        except OSError, e:
            if e.args[0] != 2:
                raise e
        self.marker = '$> '

    def tearDown(self):
        destroy_database(echo=False)

    def test_rucio_version(self):
        """CLI: Get Version"""
        cmd = 'bin/rucio --version'
        exitcode, out, err = execute(cmd)
        nose.tools.assert_equal(err, 'rucio %s\n' % version.version_string())

    def test_rucio_ping(self):
        """PING (CLI): Rucio ping"""
        cmd = 'rucio --host http://localhost ping'
        print  self.marker + cmd
        exitcode, out, err = execute(cmd)
        print out,
        nose.tools.assert_in(version.version_string(), out)

    def test_add_account(self):
        """ACCOUNT (CLI): Add account"""
        cmd = 'rucio-admin account add jdoe'
        print  self.marker + cmd
        exitcode, out, err = execute(cmd)
        print out,
        nose.tools.assert_equal('Added new account: jdoe\n', out)

    def test_whoami(self):
        """ACCOUNT (CLI): Test whoami"""
        cmd = 'rucio whoami'
        print  self.marker + cmd
        exitcode, out, err = execute(cmd)
        print out,
        nose.tools.assert_regexp_matches(out, re.compile('.*account.*'))

    def test_add_identity(self):
        """ACCOUNT (CLI): Test add identity"""
        cmd = 'rucio-admin account add jdoe'
        exitcode, out, err = execute(cmd)
        cmd = 'rucio-admin identity add --account jdoe --type gss --id jdoe@CERN.CH'
        print  self.marker + cmd
        exitcode, out, err = execute(cmd)
        print out,
        nose.tools.assert_equal('Added new identity to account: jdoe@CERN.CH-jdoe\n', out)

    def test_add_scope(self):
        """ACCOUNT (CLI): Test add identity"""
        cmd = 'rucio-admin account add jdoe'
        exitcode, out, err = execute(cmd)
        cmd = 'rucio-admin identity add --account jdoe --type gss --id jdoe@CERN.CH'
        print  self.marker + cmd
        exitcode, out, err = execute(cmd)
        print out,
        nose.tools.assert_equal('Added new identity to account: jdoe@CERN.CH-jdoe\n', out)

    def test_add_rse(self):
        """RSE (CLI): Add RSE"""
        cmd = 'rucio-admin rse add MOCK'
        print  self.marker + cmd
        exitcode, out, err = execute(cmd)
        print out,
        nose.tools.assert_equal('Added new RSE: MOCK\n', out)

    def test_list_rses(self):
        """RSE (CLI): List RSEs"""
        cmd = 'rucio-admin rse add MOCK'
        exitcode, out, err = execute(cmd)
        cmd = 'rucio-admin rse list'
        print  self.marker + cmd
        exitcode, out, err = execute(cmd)
        print out,
        nose.tools.assert_regexp_matches(out, re.compile('.*MOCK.*'))

    def test_upload(self):
        """RSE (CLI): Upload"""
        cmd = 'rucio-admin rse add MOCK'
        exitcode, out, err = execute(cmd)
        cmd = 'rucio upload'
        print  self.marker + cmd
        exitcode, out, err = execute(cmd)
        print out,

    def test_download(self):
        """RSE (CLI): Download"""
        cmd = 'rucio download'
        print  self.marker + cmd
        exitcode, out, err = execute(cmd)
        print out,
