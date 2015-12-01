# mutatio-python
Dynamically update content in html page of a python app.

## Getting Started (Developers)

1. Clone down the repo: `git clone git@github.com:Kazanz/mutatio-python.git`.
2. Install the reqs: `pip install -r reqs/dev.txt`.
3. Start the MongoDB VM: `vagrant up`. 
4. Make sure you have the correct `MUTATIO_PORT` specified in the config.
5. Run the app: `cd demo && python app.py`.
6. You can view the admin panel at: `http://127.0.0.1:5000/admin/mutatio`.


## Enviroment Variables

- MUTATIO_DB
- MUTATIO_HOST
- MUTATIO_PORT
- MUTATIO_TWEMPLATE
- MUTATIO_TEMPLATE_TAGS


## TODO

[ ] Generate the text fields in the admin panel.

[ ] Rerender from a save on the admin panel.
