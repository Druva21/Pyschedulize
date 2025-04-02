# Familiarization of Chef

## 1) What is Chef?

Chef is a powerful automation tool used for configuring, managing, and deploying applications across different systems. It follows an **Infrastructure as Code (IaC)** approach, allowing users to define system configurations in code. Chef helps automate tasks like software installation, server configuration, and application deployment, ensuring consistency and scalability in DevOps workflows.

---

## 2) Why Chef Workstation Instead of Chef Infra Server?

### i) Chef has two primary setups:
- **Chef Infra Server**: Used for managing multiple nodes (servers) remotely. It requires setting up a central server where nodes pull configurations.
- **Chef Workstation**: A local development environment for testing and running Chef cookbooks without setting up a server.

### ii) For running this application, we chose Workstation because:
- It allows testing and running Chef code locally without a separate server.
- There’s no need for managing multiple machines—ideal for single-node deployments.
- It simplifies configuration by using local mode (`--local-mode`), avoiding Chef Server setup complexities.
- Faster and easier to debug since everything runs on one machine.

---

## 3) Basic Steps to Deploy an Application Using Chef

- Install Chef Workstation
- Create a Chef Repository
- Create a Cookbook for Deployment
- Write a Recipe to Install and Deploy an Application
- Run the Recipe Locally
- Verify Deployment

These are the fundamental steps in deploying an application using Chef. Let’s see how to deploy one by taking an application.

In this project, I have used this repository:  
[https://github.com/Druva21/Pyschedulize](https://github.com/Druva21/Pyschedulize)

### Suggestions/Requisites:
- Open PowerShell as **Admin** while running the application.
- Try not to run Chef in the directory `C://Users//name` as the application may require additional permissions to run there. (As we need to run as Admin, and that path is user-specific.)

---

### Step-1: Install Chef Workstation
1. To install Chef Workstation, go to the official Chef site:  
   [https://community.chef.io/downloads/tools/workstation](https://community.chef.io/downloads/tools/workstation)  
   Visit this link, fill in your basic details, and download the application.

2. Run the installer (`.msi`) and complete the setup.
3. Verify the installation:  
   ```powershell
   chef --version
   ```

---

### Step-2: Create a Chef Repository
First, open PowerShell as **Admin**.

1. Generate a Chef repository:  
   ```powershell
   chef generate repo <repo-name>
   ```
2. Change your current working directory to that repository.
3. You’ll notice that cookbooks are generated in the repository you created.
4. These cookbooks store our recipes (applications).

---

### Step-3: Create a Cookbook for Deployment
1. Navigate to the `cookbooks` directory and generate your recipe (application):  
   ```powershell
   chef generate cookbook <your-project-name>
   ```
2. Now, you’ll see your recipe has been created.

---

### Step-4: Write a Recipe to Install and Deploy an Application
- For running your application, you need to write a Ruby file (`default.rb`).
- When generating a cookbook, it follows this structure by default and already contains a `default.rb` file.
- Modify `default.rb` according to your application. This is similar to a Jenkins Pipeline—you must write the script correctly, or you may encounter errors.

- Below is an example Ruby script for our application.

**Note**: If your application requires additional installations, keep them in a separate Ruby script at the same modularity level (e.g., `script_1.rb` in our application). Import that script into `default.rb`.

- Using multiple scripts ensures better organization and maintainability (especially for large applications).

---

### Step-5: Run the Recipe Locally
- Run the recipe locally using:  
   ```powershell
   chef-client --local-mode --runlist 'recipe[<your-recipe-name>]'
   ```
- In my Ruby script, I’ve used multiple log statements to verify the working of each stage.
- While cloning from Git, it will display a Git “action sync” message as it syncs with the repository specified in the Ruby script.

---

### Step-6: Verify Deployment
- Go to the port specified in your main file to verify deployment.
- In this example, I’ve used port `5000` to run the application.

Once you verify your deployment, terminate the process. If the application is still running on the given port, try to kill the process manually. Below are the steps to do so:

#### 1) Check Running Processes on Port
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess
```
This will display the running applications on the port.

#### 2) Kill the Process
```powershell
Stop-Process -Id <PID> -Force
```

#### 3) Check if Your Port is Free
```powershell
Get-NetTCPConnection -LocalPort 5000
```
- If you still see something, the port hasn’t released the process yet. It may release after some time.
- **Note**: Sometimes, Windows reserves ports for a short period. If you don’t want to wait, restart your system to clear the port.

---

This README provides a step-by-step guide to deploying an application using Chef Workstation, based on the `Pyschedulize` repository. Follow the instructions carefully, and ensure you run commands with the required permissions.

--- 
