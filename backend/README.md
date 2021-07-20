# Delve 2.0
## Delve Development Setup guide

1. Clone the GitHub repository `git clone https://github.com/shepherddev1/D-Web.git` 
2. Download postgresapp from `https://postgresapp.com/downloads.html(https://postgresapp.com/downloads.html`
3. Follow setup instructions from step 2
4. Run the setup script `bash setup`
5. Activate the virtual environment with `source venv/bin/activate`
6. Apply migrations to new database with `./manage.py migrate`
7. Start the local server `./manage.py runserver`

## Delve Desktop Setup guide
1. Unzip the `delve_dekstop.zip`
2. Move the delve.app to the applications folder
3. Control click to open around apple gatekeeper

## Uncompleted: 
1. Migrate the scientist, cell_line, and combo tables into new database
2.  Create a form to retrieve new experiment results in upload
3. Create a post request to display report page (display.html)
4. Create script to upload new experiment data into database, each new entry should update the experiment, experiment bundle, experiment edit history, and either combo or IC50 tables
