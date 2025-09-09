# Getting Started 

---

## 1. Create a GitHub Profile

GitHub is an online platform where developers can host, share, and collaborate on code projects.

1. Go to [https://github.com](https://github.com).  
2. Click **Sign up** (top-right corner).  
3. Enter your **email, username, and password**.  
4. Follow the steps to verify your account.  
5. Once done, you’ll have your **GitHub profile**!  

---

## 2. Install VS Code 

VS Code (Visual Studio Code) is a lightweight editor for coding.

1. Download VS Code from https://code.visualstudio.com
2. Install it using the default options.
3. Open VS Code.
4. Install recommended extensions:
- `autoDocstring`
- `Black Formatter`
- `Jupyter`
- `Pylance`

---

## 3. Install Conda 
Conda is a package and environment manager.

1. [Sign-up to Anaconda](https://www.anaconda.com/download). You can sign up with GitHub account or with your email address.
2. Verify your email address.
3. Download the installer ``Distribution Installers'' (left column)
4. Install it using the default options.
5. To check installation, run from the terminal:

```bash
conda --version
```

## 4. Install git
For MacOS users, check that git is installed by running in the terminal:
```bash
git --version
```

For Windows users, 
1. Install Git from https://git-scm.com/download/win
2. During installation, select “Git from the command line and also from 3rd-party software” to make it available in VS Code’s terminal.
3. check that git is installed by running in the terminal:
```bash
git --version
```

## 4. Set-up the Repository
### 4.a. Find and Watch the Repository 
A repository (or “repo”) is a storage space on GitHub where all the files, code, and history for a project are kept and managed.

1. Log in to GitHub.  
2. Use the search bar (top of the page) and type: 2025_Statistics_EIB11FA005
3. Click on the repository with the correct name.  
4. On the top-right of the repo page, click the **👁 Watch** button.  
- Choose **All Activity** so you’ll get updates whenever something changes.  

### 4.b Clone the Repository in VS Code
1. Open **VS Code**.  
2. Open the **Terminal** in VS Code (View > Terminal).  
3. Create a folder where you want to save the repo and clone:
```bash
cd
mkdir git
cd git
git clone https://github.com/melodiemonod/2025_Statistics_EIB11FA005.git
```


### 4.c. Install Environment from environment.yml 
A Conda environment is an isolated workspace that contains specific versions of Python and packages, and a `.yml`  file is a configuration file that lists all the packages and dependencies needed to recreate that environment.

1. Open repository on **VS Code**, Start > Open > Select the repository
2. Open Command Palette (press Ctrl+Shift+P / Cmd+Shift+P).
3. Type Python: Select Interpreter.
4. Choose the Conda environment ``2025_Statistics_EIB11FA005''.
