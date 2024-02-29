# mfpoj

A simple online judge system.

# Host Page
https://mfpoj.com

## First step

Clone the repo to your computer:
```
git clone git@github.com:nachovy/mfpoj.git
cd mfpoj
```

Satisfy prerequisites:
```
sudo pip3 install $(cat requirements.txt)
```

Then run command line:
```
python3 manage.py makemigrations oj
python3 manage.py makemigrations contest
python3 manage.py sqlmigrate oj 0001
python3 manage.py sqlmigrate contest 0001
python3 manage.py migrate
```

If you want to create a super user:
```
python3 manage.py createsuperuser
```

To run server on your computer:
```
python3 manage.py runserver
```

To start judging program (you may need root permission because the Docker root directory is in /tmp):
```
sudo apt-get install docker.io
docker build -t mfpoj .
sudo python3 judge.py
```
Now only C++ and Python are supported.

## FAQ

If PermissionError when adding testcases:
```
cd /
sudo chmod -R 777 var
```

If OperationalError:
```
python3 manage.py makemigrations oj
python3 manage.py makemigrations contest
python3 manage.py sqlmigrate oj 0001
python3 manage.py sqlmigrate contest 0001
python3 manage.py migrate
```
