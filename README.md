## How to run this project

1. Create python **virtual environment**

```shell
python3 -m venv venv
```

2. Activate the virtual environment
   Window

```shell
\venv\Scripts\activate.bat
```

MacOS/Linux

```shell
. venv/bin/activate
```

3. Install dependencies:
   change directory to fyp-website

```shell
pip install -r requirements.txt
```

3.1 Create `.env` file, copy and paste these lines into file

```
SECRET_KEY=simplesecret
DEBUG=True
DATABASE_URL=mysql://root:<password>@localhost:3306/fyp
```

Remember to populate the records of the `sql` file in the `database` directory

```shell
python main.py
```

See the page on `http://127.0.0.1:8000`

Before committing, please make the new branch.

Demo image:

![](https://github.com/ntvviktor/fyp-website/blob/main/demo.png)

## How to use database migrations
delete folder migrations (delete all the existing fyp schema)

```shell
# for Windows users
$env:FLASK_APP = "main.py"
# for MAC-OS
export FLASK_APP=main.py
```

```shell
flask db init 
OR
python -m flask db init 
```
Instead of each time we create new class in the webapp -> models folder, can use Flask-Migration
```shell
flask db migrate -m "adding message"
OR
python -m flask db migrate -m "adding message"
``` 

To create migration files, the run 
```shell
flask db upgrade
OR
python -m flask db upgrade
``` 
to apply into database.

Then run:
```shell
python insert_book.py
python insert_book_v2.py
python insert_book_v3.py
python insert_reviews.py
python insert_new_arrivals.py
python insert_user.py
python loader.py
```

Install Elasticsearch and run:
```
python loader.py
```
