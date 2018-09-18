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

from ofxparse import OfxParser
from oslo_config import cfg

_default = [
    cfg.StrOpt("file", required=True),
    cfg.StrOpt("locale", default="en_US"),
    cfg.MultiStrOpt("column_name"),
]

_column_names = [
    cfg.StrOpt("type", help="TRNTYPE"),
    cfg.StrOpt("date", help="DTPOSTED"),
    cfg.StrOpt("amount", help="TRNAMT"),
    cfg.StrOpt("id", help="FITID"),
    cfg.StrOpt("memo", help="MEMO"),
]

_type_datetime = [
    cfg.StrOpt("fmt"),
]

_type_currency = [
    cfg.StrOpt("symbol"),
]


def format_row(conf, r):
    formatted = []

    if not hasattr(conf.type_currency, "fmt"):
        conf.type_currency.fmt = conf.type_currency.symbol + "{:n}"

    for item in r:
        if isinstance(item, datetime):
            fmt = conf.type_datetime.fmt
        elif isinstance(item, Decimal):
            fmt = conf.type_currency.fmt
        else:
            fmt = "{}"

        formatted.append(fmt.format(item))

    return formatted


def main():
    conf = cfg.ConfigOpts()

    conf.register_opts(_default)
    conf.register_opts(_column_names, "column_names")
    conf.register_opts(_type_datetime, "type_datetime")
    conf.register_opts(_type_currency, "type_currency")

    conf(default_config_dirs=["etc"])

    locale.setlocale(locale.LC_ALL, conf.locale)

    with codecs.open(conf.file, encoding="utf-8") as f:
        ofx = OfxParser.parse(f)

        print(",".join([conf.column_names[n] for n in conf.column_name]))

        for transaction in ofx.account.statement.transactions:
            trn = [transaction.__getattribute__(c) for c in conf.column_name]

            print(",".join(format_row(conf, trn)))


if __name__ == "__main__":
    main()
