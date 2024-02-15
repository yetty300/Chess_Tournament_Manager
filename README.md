## Setting up the IDE (if preferred):

    Go to https://www.jetbrains.com/pycharm/ version 3.12 and download the program for your given operating system.
    Download python from https://www.python.org/downloads/ version 3.12.1 for your specific operating system.
    Open it and create a new project
    Download the code
    Extract the code to preferred location
    In the IDE go to file open and navigate to the location you extracted the code from and select the main.py (optional) Navigate the the extracted folder location and double click the main.py file and it will run automtically in the terminal

## Instructions for Terminal (Windows):

    1. Download files from this repository or create a clone using the code below.

    $ git clone https://github.com/yetty300/Chess_Tournament_Manger

    2. Navigate to the directory containing the repository.

    $ cd Chess_Tournament_Manger

    3. Using these terminal commands, create and activate a virtual environment.

    $ python -m venv env

    $ env/scripts/activate (this step may be required for some)

    4. Use the command below to install the packages according to the configuration file requirements.txt.

    $ pip install -r requirements.txt

    5. Open and run the file allcategories.py to download product data in CSV format and product images.

    $ .\main.py

 ## Instructions for Mac:

    1. Download files from this repository or create a clone using the code below.

    $ git clone https://github.com/yetty300/Chess_Tournament_Manger

    2. Navigate to the directory containing the repository.

    $ cd Chess_Tournament_Manger

    3. Using these terminal commands, create and activate a virtual environment.

    $ python -m venv env

    $ source env/bin/activate

    4. Use the command below to install the packages according to the configuration file requirements.txt.

    $ python3 -m pip install -r requirements.txt

    5. Open and run the file allcategories.py to download product data in CSV format and product images.

    ## To Generate a flake8 report
    1. Navigate to the directory containing the repository

    $ cd Chess_Tournament_Manger

    2. Run the following command

    $ flake8 --max-line-length 119 --formath=html ==htmldir=flake8_report

    3. View report in the new flake8_report directory created in the repository

