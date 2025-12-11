# CSE 620 Final Project
# Leveraging ASP on Real-Time Market Data to Observe the Most Profitable Day
## Authors: Matthew O'Connor

# Project Summary
My CSE 620 final project leverages the Charles Schwab Datastream via their API. Real-time market data is stored into three excel files which can be found in Days. Each excel file (Day1, Day2, Day3) contain information pertaining to 11 companies. That information being the Bid Price, Ask Price, Bid Size, Ask Size, High Price, Low Price, and Close Price. This information is read line by line via the functions in `file_reader.py`. The information on each line is interpreted and the data is prepared in Answer Set Prolog (ASP) format via the functions within `asp_file_functions.py`. Once the information is formatted an ASP encoding is created via `asp_file_writer.py`, the ASP file can be found in ASP Encoding. After, the ASP file is run and the answer set is both parsed and interpreted via the functions within `asp_output_parsing.py`. Depending on the output from the ASP program information may be appended to our encoding along with the new information from the excel however it is possible nothing new will be added. As the script is iterating over each line in the excel the initial budget will first be output followed by all buying and selling actions and finally the profit of the day in dollars.

# About this repository
This README is a duplicate of the README found in the ProjectFunctionality repository with some slight edits. The point of this repository is to setup a Python script to interact with the Charles Schwab API and store real-time market data for three different days to be used in the project functionality. The script recorded data for 11 companies each day and stored the data in separate excel files titled Day1.xslx, Day2.xslx, and Day3.xlsx. If you are interested in checking out the functionality repository click [here](https://github.com/MOconnorUS/ProjectFunctionality)

---
# Below will showcase how to clone the project, download Python, setup your own virtual environment, and run the project
*Please note this README assumes you already have a Charles Schwab account with a valid API token*

# How to clone a repository
*Please note this is only for Windows devices*
1. Download and install [Git](https://git-scm.com/install/windows)
2. Open Command prompt type `cmd` into the search bar on your windows device
3. Navigate to your the folder you wish to clone the repository in this can be done by typing `cd file_path_to_directory`
4. Click on the green code button on the repository shown in the image below  
![Green Code Button](./assets/images/Green_Code_Button.png "Green Code Button")
5. Copy the github link provided in the drop down by clicking the button circled in the image below  
![Copy Clone URL](./assets/images/Copy_Clone_URL.png "Copy Clone URL")
6. Type: git clone github_link *github_link is the url provided by github which can be pasted by right clicking on the command prompt*

# Download Python and add it to your PATH
1. Download and install [Python](https://www.python.org/downloads/)
**While downloading ensure you either add Python to your PATH or save the file location you downloaded it to**

If you did NOT add Python to your PATH do the following
1. Copy the file path to your Python installation
2. Edit your system environment variables by searching "Environment variables" in your windows search
3. Click environment variables as seen in the screenshot below
![Environment Variables](./assets/images/Environment_Variables.png "Environment Variables")
4. Select the Path under System Variables and edit it as seen in the screenshot below
![Edit Path](./assets/images/Edit_Path.png "Edit Path")
5. Select New and then paste your file pathing into the text field
6. Press "Ok" on all three open windows to close them
7. If you had a cmd window open, restart it

# Setup your own virtual environment
1. Open a command prompt window by typing `cmd` into your windows search
2. Navigate into the directory where you cloned the GitHub project via `cd path_to_directory`
3. Type the following: `python -m venv virtual_env`
*You can name 'virtual_env' whatever you would like*
4. Once it finishes loading you need to activate the environment by typing the following: `cd virtual_env/scripts` followed by `activate`
5. Now that your environment is active type `cd ../..` to return to the project directory
6. Finally for this project you will want to install all necessary libraries which can be done via typing `setup.bat`

# How to run
If you have completed everything above then you are ready to run your project! To do so simply type the following into the cmd window: `python schwab_interface.py` and if you wish to change the day's worth of companies being observed simply uncomment the other day's or edit the list of tickers. As the project runs it should continually print that data has been appended to the filename listed in the code. Once you are finished with the data stream press ctrl + c to shut the script down.
