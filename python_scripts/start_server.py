import subprocess

# Define the commands to run
commands = [
    r"C:\appian\services\bin\start.bat -p password -s all",
    r"C:\appian\data-server\bin\start.bat",
    r"C:\appian\search-server\bin\start.bat",
    r"C:\appian\tomcat\apache-tomcat\bin\start-appserver.bat"
]

# Run each command sequentially
for command in commands:
    print(f"Running: {command}")
    process = subprocess.run(command, shell=True)
    if process.returncode != 0:
        print(f"Command failed with return code {process.returncode}: {command}")
        break
    print(f"Completed: {command}")