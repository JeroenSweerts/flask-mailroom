import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/create_donation/', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        users_list = [user.name for user in Donor.select()]
        if request.form['name'] not in users_list:
            print("User is not in the list")
            return redirect(url_for('create'))
        elif request.form['name'] in users_list:
            print("User is in the list")
            donor = Donor.select().where(Donor.name == request.form['name']).get()
            value = int(request.form['donation'])
            Donation(donor=donor.id, value=value).save()
            return redirect(url_for('all'))
    elif request.method == "GET":
        return render_template('create_donation.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
