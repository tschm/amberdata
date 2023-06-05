# -*- coding: utf-8 -*-
from __future__ import annotations

import json


def read_json(name):
    with open(name) as f:
        return json.load(f)
