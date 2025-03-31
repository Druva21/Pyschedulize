#
# Cookbook:: pyschedulize
# Recipe:: default
#
# Copyright:: 2025, The Authors, All Rights Reserved.


log 'Starting the Pyschedulize setup...' do
    level :info
  end
  
  # Clone the GitHub repository
  git 'C:/pyschedulize' do
    repository 'https://github.com/Druva21/Pyschedulize.git'
    revision 'main'
    action :sync
  end
  
  log 'Repository cloned successfully.' do
    level :info
  end

  #Importing the other scripts
#    require_relative 'script_1'
  
  # Install dependencies
  execute 'install_requirements' do
    command 'pip install -r C:/pyschedulize/requirements.txt'
    cwd 'C:/pyschedulize'
    action :run
  end
  
  log 'Dependencies installed successfully.' do
    level :info
  end
  
  # Run the application
  execute 'run_pyschedulize' do
    command 'start /b python C:/pyschedulize/app.py'
    cwd 'C:/pyschedulize'
    action :run
  end
  
  log 'Pyschedulize application started successfully.' do
    level :info
  end
  
  # Stop any existing application running on port 5000
execute 'stop_pyschedulize' do
    command 'for /f "tokens=5" %a in (\'netstat -ano ^| findstr :5000\') do taskkill /PID %a /F'
    ignore_failure true # Prevents errors if no process is found
    action :run
  end
  