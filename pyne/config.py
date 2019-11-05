# Copyright (c) 2019 4masaka
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import dataclasses


@dataclasses.dataclass
class Config:
    host: str = "legy-jp-addr.line.naver.jp"
    line_app: str = "CHROMEOS\t2.3.0\tChrome_OS\t1"
    user_agent: str = "Mozilla/5.0 Chrome/77.0.3865.120"
    system_name: str = "pyne"

@dataclasses.dataclass
class Endpoints:
    main: str = "/S4"
    registration: str = "/api/v4/TalkService.do"
    operations: str = "/P4"
    no_auth: str = "/api/v4p/rs"
    auth_verify: str = "/Q"
