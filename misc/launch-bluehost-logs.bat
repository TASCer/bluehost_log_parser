cd /D "D:\PycharmProjects\bluehost-log_parser\src"
echo %cd%
call conda activate bluehost_logs311
python.exe "main.py"
if NOT ["%errorlevel%"] == ["0"] pause