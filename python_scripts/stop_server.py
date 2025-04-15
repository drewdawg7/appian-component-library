import subprocess

# Define the commands to run
commands = [
    r"C:\appian\tomcat\apache-tomcat\bin\stop-appserver.bat",
    r"C:\appian\search-server\bin\stop.bat",
    r"C:\appian\data-server\bin\stop.bat",
    r"C:\appian\services\bin\stop.bat -p password -s all"
]

# Run each command sequentially
for command in commands:
    print(f"Running: {command}")
    process = subprocess.run(command, shell=True)
    if process.returncode != 0:
        print(f"Command failed with return code {process.returncode}: {command}")
        break
    print(f"Completed: {command}")