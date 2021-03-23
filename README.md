# sogou-tr
<!--- sogou-tr-simple  sogou_tr  sogou_tr sogou_tr --->
[![tests](https://github.com/ffreemt/sogou-tr-simple/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/sogou_tr.svg)](https://badge.fury.io/py/sogou_tr)

sogou translate no frills

## Installation

```bash
pip install sogou-tr
```

## Usage

```python
from sogou_tr.sogou_tr import sogou_tr

text = "An employee at Spataro's No Frills, located at 8990 Chinguacousy Rd, has tested positive for the virus."
print(text, "\n")
print("to zh:", sogou_tr(text), "\n")
print("to de:", sogou_tr(text, to_lang="de"), "\n")

# to zh: 位于金瓜库西路8990号的斯帕塔罗百货公司的一名员工检测出病毒呈阳性。
# to de: Ein Mitarbeiter von Spataro es No Frills, gelegen 8990 Chinguacousy Rd, hat positiv auf das Virus getestet.
```

Consult sogou fanyi's homepage for language pairs supported.
