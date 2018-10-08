# Codecademy Checker

Automate checking group of users' learning process in [Codecademy](https://www.codecademy.com).

## Getting Started


### Prerequisites

What things you need to install the software and how to install them
1. Python 3.*
2. Pip

### Installing

1. Clone the repo
    ```
    git clone git@github.com:spiderPan/Codecademy-Checker.git
    ```
2. Install requirements packages within the repo
    ```
    cd Codecademy-Checker
    pip install -r requirments.txt
    ```

## Running the tests
1. Configure the course list within the function `get_check_course_list`, each course will be an dict like the following. 
    ```bash
    {
        'name': 'learn-sql',
        'url': 'https://www.codecademy.com/learn/learn-sql',
        'courses': [
            'Manipulation',
            'Queries',
            'Aggregate Functions',
        ]
    }
    ```
        
    * The `name` field can be whatever.
        
    * The `url` has to match the course's url in codecademy site.
        
    * The `courses` list will contain all sub courses name you want to check

2. Prepare all users' credentials in `users.csv` within the same folder. Each row will be format like
    ```bash
    UserID, Username/Email, Password
    ```
    * The `UserID` is just for reference.
        
3. Run the checker like
    ```bash
    python init.py
    ```
## Future Plan
The project can be improved by the following fields
~~1. Report invalided user row in `users.csv`.~~
2. Throw an exception when login with user's credential failed.
3. Automatically marking completion by percentage