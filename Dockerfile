FROM python:3.11-slim-bullseye

LABEL authors="viktorngo"
RUN apt-get update -y && apt-get upgrade -y && apt-get dist-upgrade -y
RUN apt-get install -y wget curl
RUN wget https://r.mariadb.com/downloads/mariadb_repo_setup
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup --mariadb-server-version="mariadb-10.6"
# Update the package index and install dependencies
RUN apt-get install -y \
    apt-transport-https \
    build-essential \
    gcc \
    libmariadb3 \
    libmariadb-dev \
    libffi-dev \
    liblapack-dev \
    libopenblas-dev \
    default-libmysqlclient-dev \
    pkg-config \
    cmake \
    mariadb-server \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file first for Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . .

# Copy the startup script and make it executable
COPY startup.sh .
RUN chmod +x startup.sh

# Expose the port your application will run on
EXPOSE 8080

# Specify the command to run on container start
CMD ["./startup.sh"]