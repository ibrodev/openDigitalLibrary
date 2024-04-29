# Open Digital Library

## Requirements
This project requires the following technologies to run. Make sure all are installed on your machine
- NodeJS
- Redis


## Development workflow

1. Clone the project on your local machine
    ```bash
    git clone https://github.com/ibrodev/openDigitalLibrary.git
    ```
2. Create a virtual environment
    ```bash
    python3 -m venv .venv
    ```
3. Activate the virtual environment

    __On Windows__

    ```bash
    .venv\Scripts\activate
    ```
    __On Linux__
    ```bash
    source .venv/bin/activate
    ```
4. Install python modules and libraries
   ```bash
   pip install -r requirements.txt
   ```
5. Install Node modules
   ```bash
   npm install
   ```
6. Rename .env.example file to .env and edit to include correct environment variables
7. Make sure redis is running, you can use a redis docker container
   ```bash
   docker run -d -p 6379:6379 redis
   ```
8. Compile tailwindcss and watch for changes
   ```bash
   npx tailwindcss -i .\src\css\base.css -o .\static\css\base.css --watch
   ```
9. Start the django celery server instance
    - __Note:__ you can omit --pool=solo argument if you are on a Windows Machine
    ```bash
    celery -A core worker -l info --pool=solo
    ```
10. Run django's http server
    ```bash
    python3 manage.py runserver
    ```