#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import codecs
from datetime import datetime
from decimal import Decimal
import locale

from config import register_opts

from babel.numbers import format_currency
from ofxparse import OfxParser
from oslo_config import cfg


def format_row(conf, row, currency):
    formatted = []

    for value in row:
        if isinstance(value, datetime):
            formatted.append(conf.type_datetime.fmt.format(value))
        elif isinstance(value, Decimal):
            formatted.append(format_currency(value, currency,
                                             locale=conf.locale))
        else:
            formatted.append(value)

    return formatted


def main():
    conf = cfg.ConfigOpts()

    register_opts(conf)

    conf(default_config_dirs=["etc"])

    locale.setlocale(locale.LC_ALL, conf.locale)

    with codecs.open(conf.file, encoding=conf.encoding) as f:
        try:
            ofx = OfxParser.parse(f)
        except Exception as e:
            import sys
            raise type(e)(
                      str(e) + ' parsing file %s' % conf.file
                  ).with_traceback(sys.exc_info()[2])

        print(",".join([conf.column_names[n] for n in conf.columns]))

        for transaction in ofx.account.statement.transactions:
            trn = [transaction.__getattribute__(c) for c in conf.columns]

            print(",".join(format_row(conf, trn, ofx.account.curdef)))


if __name__ == "__main__":
    main()
