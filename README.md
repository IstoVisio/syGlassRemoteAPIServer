"# syGlassRemoteAPIServer" 

python > 3.6

current dependencies:

pip install fastapi
pip install uvicorn
pip install email_validator
pip install requests

or

pip3 install fastapi[all]

Run the server with:

uvicorn server:app --reload

then visit  http://127.0.0.1:8000/