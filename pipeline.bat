REM © 2023 - 2024 Fraunhofer-Gesellschaft e.V., München
REM © 2024 Fraunhofer-Gesellschaft e.V., M├╝nchen
REM
REM SPDX-License-Identifier: AGPL-3.0-or-later

REM This batch file can be used to run some of the pipline commands locally
REM Run it with the command ./piepline.bat from within PyCharm terminal.

echo "Installing python requirements..."
pip install -e .[dev] | findstr /V /C:"Requirement already satisfied"

echo "Formatting code..."
isort .
black src -S -l 120
black test -S -l 120

echo "Checking code quality with  pylint..."
pylint src
pylint test --recursive=true


REM echo "Checking licenses..."  REM only works on server where no extra packages are installed
REM python check/check_licenses.py

echo "Creating reuse annotations"
python -m reuse annotate --copyright="Fraunhofer-Gesellschaft e.V., München" --copyright-style=symbol --merge-copyrights --license=AGPL-3.0-or-later --skip-unrecognised --recursive .

REM echo "Running unit tests and determining test coverage..."
REM pytest --cov

if (%1==skip_pause) (
 echo "Finished commands."
) else (
 echo "Finished commands."
 pause
)

