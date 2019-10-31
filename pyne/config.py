# Copyright (c) 2019 4masaka
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import dataclasses


@dataclasses.dataclass
class Config:
    host: str = "legy-jp-addr.line.naver.jp"
    line_app: str = "CHROMEOS\t2.2.2\tChrome_OS\t1"
    user_agent: str = "Mozilla/5.0 Chrome/77.0.3865.120"
    system_name: str = "pyne"

@dataclasses.dataclass
class Endpoints:
    pass
