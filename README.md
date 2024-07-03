python3.12 -m uvicorn main:app --host 0.0.0.0 --reload
python3.12 -m uvicorn app.main:app --host 0.0.0.0 --reload

-> Virtual ENV:
pip install virtualenv
python -m venv myenv
source myenv/bin/activate (Linux / MacOS)
myenv\Scripts\activate.bat (Windows)
myenv\Scripts\activate.ps1 (Windows from powershell)

deactivate (To exit from venv)

-> Place your versions in a .txt file for other devs:
pip freeze (Show the versions of all of your packages)
pip freeze > requirements.txt (Write those versions in a seperate .txt file)
pip install -r requirements.txt (Install all the versions from that .txt file)

