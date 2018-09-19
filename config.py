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

from oslo_config import cfg

_cli_opts = [
    cfg.StrOpt("encoding",
               short="e",
               default="utf-8",
               help="Input file encoding."
                    "E.g. 'utf-8' or 'latin-1'."),

    cfg.StrOpt("file",
               help="Input OFX file to be converted to CSV.",
               required=True,
               positional=True),
]

_default_opts = [
    cfg.StrOpt("locale",
               default="en_US",
               help="Localization for number formatting."
                    "E.g.: en_US -> 1,000.00, pt_BR -> 1.000,00"),

    cfg.ListOpt("columns",
                default=["id", "date", "type", "memo", "amount"],
                help="Column names in the first row of the output."),
]

_column_names_opts = [
    cfg.StrOpt("type",  # TRNTYPE
               default="Type",
               help="Represents the transaction type. Possible values are:\n"
               "\n+----------------------------------------------------------+"
               "\n| CREDIT       | Generic credit                            |"
               "\n| DEBIT        | Generic debit                             |"
               "\n| INT          | Interest earned or paid                   |"
               "\n|              | Note: Depends on signage of amount        |"
               "\n| DIV          | Dividend                                  |"
               "\n| FEE          | FI fee                                    |"
               "\n| SRVCHG       | Service charge                            |"
               "\n| DEP          | Deposit                                   |"
               "\n| ATM          | ATM debit or credit                       |"
               "\n|              | Note: Depends on signage of amount        |"
               "\n| POS          | Point of sale debit or credit             |"
               "\n|              | Note: Depends on signage of amount        |"
               "\n| XFER         | Transfer                                  |"
               "\n| CHECK        | Check                                     |"
               "\n| PAYMENT      | Electronic payment                        |"
               "\n| CASH         | Cash withdrawal                           |"
               "\n| DIRECTDEP    | Direct deposit                            |"
               "\n| DIRECTDEBIT  | Merchant initiated debit                  |"
               "\n| REPEATPMT    | Repeating payment/standing order          |"
               "\n| HOLD         | Only valid in <STMTTRNP>; indicates the   |"
               "\n|              | amount is under a hold                    |"
               "\n|              | Note: Depends on signage of amount and    |"
               "\n|              | account type                              |"
               "\n| OTHER        | Other                                     |"
               "\n+----------------------------------------------------------+"
               ),

    cfg.StrOpt("date",  # <DTPOSTED>
               default="Date",
               help="Date transaction was posted to account."),

    cfg.StrOpt("amount",  # <TRNAMT>
               default="Amount",
               help="Amount of transaction, amount"),

    cfg.StrOpt("id",  # <FITID>
               default="ID",
               help="Financial Institution Transaction ID."),

    cfg.StrOpt("memo",  # <MEMO>
               default="Memo",
               help="Provides additional information about a transaction"),
]

_type_datetime_opts = [
    cfg.StrOpt("fmt",
               default="{:%Y-%m-%d}",
               help="Format for datetime output."),
]


def register_opts(conf):
    conf.register_cli_opts(_cli_opts)

    conf.register_opts(_default_opts)
    conf.register_opts(_column_names_opts, "column_names")
    conf.register_opts(_type_datetime_opts, "type_datetime")
