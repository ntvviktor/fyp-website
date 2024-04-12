How to run this project

0. Populate the sql data into your local MySQL database
   the query is in the folder `database/fypv2.sql`

1. Create python virtual environment

```shell
python3 -m venv .venv
```

2. Activate the virtual environment
   Window

```shell
.venv\Scripts\activate
```

MacOS/Linux

```shell
. .venv/bin/activate
```

3. Install dependencies
   change directory to fyp-website

```shell
pip install -r requirements.txt
```

create `.env` file, add into this file

```
SECRET_KEY=simplesecret
DEBUG=True
DATABASE_URL=mysql://root:<password>@localhost:3306/fyp
```

Remember to populate the records of the `sql` file in the `database` directory

4. Run the localhost

```shell
python main.py
```

See the page on `http://127.0.0.1:5000`

Before committing, please make the new branch.

Demo image:

![](https://github.com/ntvviktor/fyp-website/blob/main/demo.png)

Instead of each time we create new class in the webapp -> models folder, can user Flask-Migration
to run the `flask db migrate -m "adding message"` to create migration files, the run `flask db upgrade` to
apply into database.
