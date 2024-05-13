#!/bin/sh
set -e

if [ -d "/app/migrations" ]; then
  echo "Removing old migrations..."
  rm -rf /app/migrations
#  mysql -h mariadb -P 3306 -u root -p--execute "DELETE FROM alembic_version;" fyp
fi
# Only initialize the database if it doesn't already exist

flask db init
flask db migrate
flask db upgrade

# Insert data only if it doesn't already exist
python insert_book.py
python insert_book_v2.py
python insert_book_v3.py
python insert_reviews.py
python insert_new_arrivals.py
python insert_user.py
python loader.py
python main.py