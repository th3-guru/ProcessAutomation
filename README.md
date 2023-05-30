# ProcessAutomation
Data generation, aggregation and cleanup automation using python and shell scripts.
This repository contains project files including python and shell scripts to generate, aggregate and cleanup data and schedule the processes to take place everyday.

It uses python scripts for generation, aggregation and cleanup, and two options to schedule the processes to run everyday:
1. A shell script to setup a CRON job, and
2. An airflow DAG.

Both the methods require a linux environment to run.

To set up a CRON job:
1. Open terminal(Mac) or wsl terminal(windows)
2. Enter: crontab -e
3. In the crontab editor, enter:
* "0 0 * * * /path/to/run_scripts.sh"
* replace "/path/to" with where the shell script is saved.
* replace "0 0 * * *" with required timing to run the script.
* 0 indicates the minute when the cron job will run. In this case, it is set to run at minute 0(the start of the hour).
* 15 indicates the hour when the cron job will run. It is set to run at hour 15 (3 PM in 24-hour format).
* "* * *" indicates the day of the month, month, and day of the week, respectively. In this case, all asterisks (*) are used, which means the cron job will run every day, every month, and every day of the week.

To set up an airflow job:
1. Install and set up airflow in your unix based environment.
2. Open the DAGs folder and copy and paste the run_scripts.py under the DAGs subdirectory in your airflow Directory
2. Open terminal(Mac) or wsl terminal(windows)
3. Run:
	airflow web server
	airflow scheduler
4. Open your browser and go to the port where airflow is running. The default port is localhost:8080
5. Find the daily_processing DAG in the airflow UI. Turn on the DAG by toggling the switch icon.

Description of the process:
1. (Optional - personal testing purpose)The generate_data.py script generates a random dataset everyday, into the ./in folder
2. The aggregate_data.py script does all the required processes as mentioned in the case study, and aggregates the data based on top 50 songs per country and users into two separate files of the formats country_top50_YYYYMMDD.txt and user_top50_YYYYMMDD.txt respectively. These files are saved into the ./out folder.
3. Following the execution of the aggregate_data.py script, the clean_up.py script will be executed which will delete files that are older than 7 days, based on the date extracted from the name of the log files.

The in and out folders already contain test results. 
