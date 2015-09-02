import datetime
from flask import render_template, flash, request, redirect, Response
from app import app, db, models
from .forms import (BeerForm, KegForm, KegeratorForm, LoginForm,
                    FloorForm, VoteForm, RequestForm)
from . import auth
import json


@app.route('/')
def index():
    floors = models.Floor.query.all()
    kegerators = models.Kegerator.query.all()
    return render_template('index.html',
            floors=sorted(floors, key=lambda x: x.number, reverse=False),
            kegerators=sorted(kegerators, key=lambda x: x.name, reverse=False))

@app.route('/api', methods=['GET'])
def api():
    floors = models.Floor.query.all()
    kegerators = models.Kegerator.query.all()
    kegs = models.Keg.query.all()
    beer = models.Beer.query.all()
    data = {}
    for floor in floors:
        data[str(floor)] = {}
        for keger in floor.kegerators:
            data[str(floor)][str(keger)] = []
            for keg in keger.kegs:
                if keg.tapped:
                    data[str(floor)][str(keger)].append(str(keg))
    return json.dumps(data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    login_error = False
    if form.validate_on_submit():
        if auth.authenticate(form.username.data, form.password.data):
            return redirect(request.args.get("return", "/"))
        login_error = True
    return render_template('login.html',
            login_error = login_error,
            form = form)

@app.route('/logout')
@auth.requires_auth
def logout():
    auth.logout()
    return redirect('/', code=302)

@app.route('/floors')
def floors():
    '''Views all floors'''
    return render_template('floors.html',
            floors=sorted(models.Floor.query.all(), key=lambda x: x.number,
                reverse=False))

@app.route('/floor/<id>', methods=['GET', 'POST'])
def floor(id):
    '''Views particular floor'''
    floor = models.Floor.query.get_or_404(id)
    form = FloorForm(obj=floor)
    kegerators = models.Kegerator.query.all()
    #form.kegerators.choices = [(k.id, k.__repr__()) for k in kegerators]
    #form.kegerators.choices.insert(0, (0, ''))
    if form.validate_on_submit():
        form.populate_obj(floor)
        db.session.commit()
    return render_template('floor.html',
            floor = floor,
            form = form)

@app.route('/floor/add', methods=['GET', 'POST'])
@auth.requires_auth
@auth.requires_admin
def add_floor():
    '''Adds a floor'''
    # Create the form
    form = FloorForm()
    kegerators = models.Kegerator.query.all()
    #form.kegerators.choices = [(k, k.__repr__()) for k in kegerators]
    #form.kegerators.choices.insert(0, (0, ''))
    # Create the floor
    new_floor = models.Floor()
    if form.validate_on_submit():
        form.populate_obj(new_floor)
        db.session.add(new_floor)
        db.session.commit()
        return redirect("/floor/{0}".format(new_floor.id), 302)
    return render_template('floor_add.html',
            form=form)

@app.route('/kegerators')
def kegerators():
    '''Displays all kegerators'''
    return render_template('kegerators.html',
            kegerators=sorted(models.Kegerator.query.all(), key=lambda x:
                x.name, reverse=False))

@app.route('/kegerator/<id>', methods=['GET', 'POST'])
def kegerator(id):
    '''Displays a certain kegerator'''
    kegerator = models.Kegerator.query.get_or_404(id)
    form = KegeratorForm(obj=kegerator)
    floors = models.Floor.query.all()
    kegs = models.Keg.query.all()
    #form.kegs.choices = [(k.id, k.__repr__()) for k in kegs]
    #form.kegs.choices.insert(0, (0, ''))
    sorted_floors = sorted(floors, key=lambda x: x.number, reverse=False)
    form.floor_id.choices = [(f.id, f.__repr__()) for f in sorted_floors]
    form.floor_id.choices.insert(0, (0, ''))
    # Update model
    if form.validate_on_submit():
        form.populate_obj(kegerator)
        db.session.commit()
    return render_template('kegerator.html',
            kegerator = kegerator,
            form = form)

@app.route('/kegerator/add', methods=['GET','POST'])
@auth.requires_auth
@auth.requires_admin
def add_kegerator():
    # Create the form
    form = KegeratorForm()
    floors = models.Floor.query.all()
    sorted_floors = sorted(floors, key=lambda x: x.number, reverse=False)
    form.floor_id.choices = [(f.id, f.__repr__()) for f in sorted_floors]
    form.floor_id.choices.insert(0, (0, ''))
    kegs = models.Keg.query.all()
    #form.kegs.choices = [(k.id, k.__repr__()) for k in kegs]
    #form.kegs.choices.insert(0, (0, ''))
    # Create the kegerator
    new_kegerator = models.Kegerator()
    if form.validate_on_submit():
        form.populate_obj(new_kegerator)
        db.session.add(new_kegerator)
        db.session.commit()
        return redirect("/kegerator/{0}".format(new_kegerator.id), 302)
    return render_template('kegerator_add.html',
            form=form)

@app.route('/kegs')
def kegs():
    '''Displays all kegs'''
    kegs = models.Keg.query.all()
    if kegs:
        return render_template('kegs.html',
                kegs=kegs)
        '''
                kegs=sorted(kegs, key=lambda x: x.beer.name,
                    reverse=False))
                    '''
    else:
        return render_template('kegs.html',
                kegs=None)

@app.route('/keg/<id>', methods=['GET', 'POST'])
def keg(id):
    '''Views particular keg'''
    keg = models.Keg.query.get_or_404(id)
    form = KegForm(obj=keg)
    beers = models.Beer.query.all()
    sorted_beers = sorted(beers, key=lambda x: x.name, reverse=False)
    form.beer_id.choices = [(b.id, b.__repr__()) for b in sorted_beers]
    form.beer_id.choices.insert(0, (0, ''))
    kegerators = models.Kegerator.query.all()
    sorted_kegerators = sorted(kegerators, key=lambda x: x.name, reverse=False)
    form.kegerator_id.choices = [(k.id, k.__repr__()) for k in sorted_kegerators]
    form.kegerator_id.choices.insert(0, (0, ''))
    # Update model
    if form.validate_on_submit():
        form.populate_obj(keg)
        db.session.commit()
    return render_template('keg.html',
            form=form,
            keg=keg)

@app.route('/keg/add', methods=['GET', 'POST'])
@auth.requires_auth
@auth.requires_admin
def add_keg():
    # Create the form
    form = KegForm()
    beers = models.Beer.query.all()
    sorted_beers = sorted(beers, key=lambda x: x.name, reverse=False)
    form.beer_id.choices = [(b.id, b.__repr__()) for b in sorted_beers]
    form.beer_id.choices.insert(0, (0, ''))
    kegerators = models.Kegerator.query.all()
    sorted_kegerators = sorted(kegerators, key=lambda x: x.name, reverse=False)
    form.kegerator_id.choices = [(k.id, k.__repr__()) for k in sorted_kegerators]
    form.kegerator_id.choices.insert(0, (0, ''))
    # Create the keg
    new_keg = models.Keg()
    if form.validate_on_submit():
        form.populate_obj(new_keg)
        db.session.add(new_keg)
        db.session.commit()
        return redirect("/keg/{0}".format(new_keg.id), 302)
    return render_template('keg_add.html',
            form=form)

@app.route('/beers')
def beers():
    '''Displays all beers'''
    return render_template('beers.html',
            beers=sorted(models.Beer.query.all(), key=lambda x: x.name,
                reverse=False))

@app.route('/beer/<id>', methods=['GET', 'POST'])
def beer(id):
    '''Displays a certain beer or the pace to create a beer'''
    beer = models.Beer.query.get_or_404(id)
    form = BeerForm(obj=beer)
    kegs = models.Keg.query.all()
    #form.kegs.choices = [(k.id, k.__repr__()) for k in kegs]
    #form.kegs.choices.insert(0, (0, ''))
    if form.validate_on_submit():
        form.populate_obj(beer)
        db.session.commit()
    return render_template('beer.html',
            form=form,
            beer=beer)

@app.route('/beer/add', methods=['GET', 'POST'])
@auth.requires_auth
@auth.requires_admin
def edit_beer():
    form = BeerForm()
    kegs = models.Keg.query.all()
    #form.kegs.choices = [(k.id, k.__repr__()) for k in kegs]
    #form.kegs.choices.insert(0, (0, ''))
    # create the beer
    new_beer = models.Beer()
    if form.validate_on_submit():
        form.populate_obj(new_beer)
        db.session.add(new_beer)
        db.session.commit()
        return redirect("/beer/{0}".format(new_beer.id), 302)
    return render_template('beer_add.html',
            form=form)

@app.route('/request', methods=['GET', 'POST'])
@app.route('/request/<id>', methods=['GET', 'POST'])
@auth.requires_auth
def request_beer(id=None):
    form = RequestForm()
    if id and not auth.has_voted():
        myrequest = models.Request.query.filter(models.Request.name==id).first()
        myrequest.total += 1
        db.session.commit()
        auth.vote()
        return redirect("/request", 302)
    elif form.validate_on_submit():
        new_request = models.Request()
        new_request.name = form.name.data
        new_request.created = datetime.date.today()
        new_request.total = 0
        db.session.add(new_request)
        db.session.commit()
    return render_template('request.html',
            requests=sorted(models.Request.query.all(), key=lambda x:
                x.total, reverse=True),
            form=form)

'''
@app.route('/vote', methods=['GET', 'POST'])
def vote():
    beers = models.Beer.query.all()
    form = VoteForm()
    form.beer_id.choices = [(b.id, b.__repr__()) for b in beers]
    if form.validate_on_submit():
        vote = models.Vote()
        vote.created = datetime.date.today()
        vote.rating = abs(form.rating.data) % 101
        vote.beer_id = form.beer_id.data
        beer = models.Beer.query.get(form.beer_id.data)
        total_votes = models.Vote.query.filter(models.Vote.beer_id==form.beer_id.data).count()
        current_score = beer.isi_score
        new_score = (current_score * total_votes + vote.rating) / (total_votes + 1)
        beer.isi_score = new_score
        db.session.add(vote)
        db.session.commit()
    return render_template('vote.html',
            form=form,
            beers=beers)
'''
