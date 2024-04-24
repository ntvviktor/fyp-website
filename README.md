## How to run this project

0. Populate the sql data into your local MySQL database
   the query is in the folder `database/fypv2.sql`

1. Create python **virtual environment**

```shell
python3 -m venv .venv
```

2. Activate the virtual environment
   Window

```shell
\venv\Scripts\activate.bat
```

MacOS/Linux

```shell
. .venv/bin/activate
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

4. Run the localhost:
   Add `training.json` in tele the same directory as `main.py` before running

```shell
python main.py
```

See the page on `http://127.0.0.1:8000`

Before committing, please make the new branch.

Demo image:

![](https://github.com/ntvviktor/fyp-website/blob/main/demo.png)

## How to use database migrations
delete folder migrations

`flask db init`
Instead of each time we create new class in the webapp -> models folder, can use Flask-Migration
```
flask db migrate -m "adding message"
``` 

To create migration files, the run 
```
flask db upgrade
``` 
to apply into database.
