import subprocess
import sys
import os

# Function to create and activate a virtual environment
def setup_venv():
    venv_path = os.path.expanduser("~/venv")
    if not os.path.exists(venv_path):
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
    return os.path.join(venv_path, "bin", "python"), os.path.join(venv_path, "bin", "pip")

# Get Python and Pip inside venv
venv_python, venv_pip = setup_venv()

# Function to install a Python package within venv
def install_package(package_name):
    subprocess.run([venv_python, "-m", "pip", "install", "--force-reinstall", package_name], check=True)

# Function to clone a repository
def clone_repo(repo_url):
    subprocess.run(["git", "clone", repo_url], check=True)

# List of repositories to clone
repos = [
    "https://github.com/knavesec/CredMaster.git",
    "https://github.com/dirkjanm/adconnectdump.git",
    "https://github.com/axylisdead/TenantHunter.git",
    "https://github.com/SpecterOps/AzureHound.git",
    "https://github.com/ly4k/Certipy.git",
    "https://github.com/ropnop/windapsearch.git",
    "https://github.com/micahvandeusen/gMSADumper.git",
    "https://github.com/ropnop/kerbrute.git",
    "https://github.com/n00py/LAPSDumper.git",
    "https://github.com/SySS-Research/azurenum.git",
    "https://github.com/blechschmidt/massdns.git"
]

# List of Python packages to install
packages = ["azure-ad-verify-token", "msal", "bloodhound", "certipy-ad", "python-ldap"]

# Clone repositories
for repo in repos:
    clone_repo(repo)

# Install required Python packages in venv
for package in packages:
    install_package(package)

# Build and install MassDNS
if os.path.exists("massdns"):
    os.chdir("massdns")
    subprocess.run(["make"], check=True)
    subprocess.run(["sudo", "make", "install"], check=True)
    os.chdir("..")

# Install LDAPNomNom using Go
subprocess.run(["go", "install", "github.com/lkarlslund/ldapnomnom@latest"], check=True)

print(f"Setup complete! Virtual environment created at {venv_python}. Use 'source ~/venv/bin/activate' to activate it.")
