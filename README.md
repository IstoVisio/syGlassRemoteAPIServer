"# syGlassRemoteAPIServer" 

python > 3.6
64 bit only!

current dependencies:

pip install fastapi
pip install uvicorn
pip install email_validator
pip install requests
pip install numpy
pip install -i https://test.pypi.org/simple/ syGlass


Run the server with:

uvicorn server:app --reload

then visit  http://127.0.0.1:8000/