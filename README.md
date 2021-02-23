# pdfExtractCapi
This project is an automatisation to read RPS and NAS pdf for CAPImmobilier.

# Setup for an virtual environment
1. **apt-get install python3.8-venv**
2. Go in folder extract_price and run: **python3 -m venv capi-env**
3. Activate the virtual environment: **source capi-env/bin/activate**

# Install environment
1. Have pip install
2. Activate the virtual environment
3. **pip3 install -r requirements.txt** to install pandas and pylint

# Freeze an environment when you add a new library
- **pip freeze > requirements.txt**

# Deactivate venv
- **deactivate**

# Lint
There is pylint in the requirements.txt. To activate the pylint, write the command in the terminal: **pylint "file_path"**.

# .env
Copy .env.example and change by .env. Ask at David Pare the url of the BD.

# Setup
Serveless : https://serverless.com/framework/docs/getting-started/.
Install plugin serverless-python-requirements: 'sls plugin install -n serverless-python-requirements'


