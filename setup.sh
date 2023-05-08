REPO_ROOT=$(git rev-parse --show-toplevel)

# Check if you have python3 installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found"
    exit
fi

# Check if the venv is created, if not create it and install the requirements
if [ ! -d "$REPO_ROOT/venv" ]; then
    echo "Creating venv"
    python3 -m venv venv
    echo "Installing requirements"
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "Venv already exists"
    source venv/bin/activate
fi

