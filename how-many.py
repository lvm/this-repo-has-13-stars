#!/usr/bin/env python3

"""
this-repo-has-many-stars - Counts how many stars a repo has and renames it accordingly
License: BSD 3-Clause
Copyright (c) 2021, Mauro <mauro@sdf.org>
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:
1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

__author__ = "Mauro"
__version__ = "2021.02.21"
__license__ = "BSD3"

import re
import json
import datetime
import http.client
import urllib.request
from typing import Union
from typing import Literal
from typing import Callable
from typing import NoReturn
from os import getenv as env


REPO_ID = env("REPO_ID", "")
TOKEN = env("TOKEN", "")


def repository(repo_id: int) -> str:
    return f"https://api.github.com/repositories/{repo_id}"


def GET(url: str) -> Union[http.client.HTTPResponse, NoReturn]:
    "HTTP(s) GET Requests"
    request = urllib.request.Request(url)
    request.add_header("Pragma", "no-cache")
    request.add_header("User-Agent", f"this-repo-has-x-stars/{__version__}")
    with urllib.request.urlopen(request) as response:
        assert response.status == 200, "Oops! HTTP Request failed: {response.status}"

        return response.read().decode("utf-8")


def PATCH(
    url: str, data: dict, token: str
) -> Union[http.client.HTTPResponse, NoReturn]:
    "HTTP(s) PATCH Requests"
    request = urllib.request.Request(url, method="PATCH")
    req.add_header("Authorization", f"Token {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    request.add_header("Pragma", "no-cache")
    request.add_header("User-Agent", f"this-repo-has-x-stars/{__version__}")
    with urllib.request.urlopen(request, data=data) as response:
        # assert response.status == 200, "Oops! HTTP Request failed: {response.status}"

        print(response.status)
        return response.read().decode("utf-8")


def rename_repo(repo_id: int, token: str) -> Literal[None]:
    "Rename a repo based on how many stargazers has"
    response = GET(repository(repo_id))
    response = json.loads(response)

    old_name = response.get("name")
    stars = response.get("stargazers_count")

    response = PATCH(
        f"https://api.github.com/repos/owner/{old_name}",
        {"name": f"this-repo-has-{stars}-stars"},
        token,
    )

    print(response)



if __name__ == "__main__":
    assert REPO_ID and TOKEN, "Missing ENV variables!"
    rename_repo(REPO_ID, TOKEN)
