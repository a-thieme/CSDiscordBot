# Make sure powershell is allowed to execute scripts
$scope = Get-ExecutionPolicy
if ([string]$scope = "RemoteSigned") {
    "All is good."
} else {
    try {
        Set-ExecutionPolicy RemoteSigned
        Get-ExecutionPolicy
    } catch {
        Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
        Get-ExecutionPolicy
    }
}


# Get the root of the repo
$root = $(git rev-parse --show-toplevel)
cd $root

# Create the virtual env
python -m venv venv

# activate it
.\venv\Scripts\activate

# upgrade pip
python -m pip install --upgrade pip
# install what we need
pip install -r requirements.txt