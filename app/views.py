from flask import render_template, flash, request, redirect
from app import app, db, models
from .forms import BeerForm, KegForm, KegeratorForm, FloorForm
from . import auth



@app.route('/')
def index():
    floors = models.Floor.query.all()
    kegerators = models.Kegerator.query.all()
    return render_template('index.html',
            floors=floors,
            kegerators=sorted(kegerators, key=lambda x: x.name, reverse=False))

@app.route('/floors')
def floors():
    '''Views all floors'''
    return render_template('floors.html',
            floors=sorted(models.Floor.query.all(), key=lambda x: x.number,
                reverse=False))

@app.route('/floor/<id>', methods=['GET', 'POST'])
@auth.requires_auth
def floor(id):
    '''Views particular floor'''
    floor = models.Floor.query.get_or_404(id)
    form = FloorForm()
    kegerators = models.Kegerator.query.all()
    form.kegerators.choices = [(k.id, k.__repr__()) for k in kegerators]
    # fill out form
    form.number.data = floor.number
    form.kegerators = floor.kegerators
    if form.validate_on_submit():
        floor.number = form.number.data
        floor.kegerators = form.kegerators.data
        db.session.commit()

    return render_template('floor.html',
            floor = floor,
            form = form)

@app.route('/floor/add', methods=['POST'])
@auth.requires_auth
def add_floor():
    '''Adds a floor'''
    # Create the form
    form = FloorForm()
    kegerators = models.Kegerator.query.all()
    form.kegerators.choices = [(k.id, k.__repr__()) for k in kegerators]
    # Create the floor
    new_floor = models.Floor()
    if form.validate_on_submit():
        new_floor.number = form.number.data
        new_floor.kegerators = form.kegerators.data
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
@auth.requires_auth
def kegerator(id):
    '''Displays a certain kegerator or the page to create a kegerator'''
    form = KegeratorForm()
    floors = models.Floor.query.all()
    form.floor.choices = [(f.id, f.__repr__()) for f in floors]
    kegs = models.Keg.query.all()
    form.keg.choices = [(k.id, k.__repr__()) for k in kegs]
    if id == "add":
        kegerator = models.Kegerator()
    else:
        kegerator = models.Kegerator.query.get(id)
        if kegerator == None:
            return render_template('404.html'), 404
        elif request.method == "GET":
            form.clean_date.data = kegerator.clean_date
            form.co2.data = kegerator.co2
            form.co2_date.data = kegerator.co2_date
            form.floor.data = kegerator.floor_id
            form.keg.data = kegerator.keg_id
            form.name.data = kegerator.name

    if form.validate_on_submit():
        kegerator.clean_date = form.clean_date.data
        kegerator.co2_date = form.co2_date.data
        kegerator.co2 = form.co2.data
        kegerator.floor_id = form.floor.data
        kegerator.keg_id = form.keg.data
        kegerator.name = form.name.data
        if id == "add":
            db.session.add(kegerator)
        db.session.commit()

    return render_template('kegerator.html',
            form=form,
            kegerator=kegerator)

@app.route('/kegerator/<id>/edit')
def edit_kegerator(id):
    return 'Hello World!'

@app.route('/kegs')
def kegs():
    '''Displays all kegs'''
    return render_template('kegs.html',
            kegs=sorted(models.Keg.query.all(), key=lambda x: x.beer.name,
                reverse=False))

@app.route('/keg/<id>', methods=['GET', 'POST'])
@auth.requires_auth
def keg(id):
    '''Displays certain keg or the page to create a keg'''
    form = KegForm()
    beers = models.Beer.query.all()
    form.beer.choices = [(b.id, b.__repr__()) for b in beers]
    if id == "add":
        keg = models.Keg()
    else:
        keg = models.Keg.query.get(id)
        if keg == None:
            return render_template('404.html'), 404
        elif request.method == "GET":
            form.beer.data = keg.beer_id
            form.chilled.data = keg.chilled
            form.chilled_date.data = keg.chilled_date
            form.empty_date.data = keg.empty_date
            form.filled.data = keg.filled
            form.filled_date.data = keg.filled_date
            form.stocked.data = keg.stocked
            form.stocked_date.data = keg.stocked_date
            form.tapped.data = keg.tapped
            form.tapped_date.data = keg.tapped_date

    if form.validate_on_submit():
        keg.beer_id = int(form.beer.data)
        keg.chilled_date = form.chilled_date.data
        keg.chilled = form.chilled.data
        keg.empty_date = form.empty_date.data
        keg.filled_date = form.filled_date.data
        keg.filled = form.filled.data
        keg.stocked_date = form.stocked_date.data
        keg.stocked = form.stocked.data
        keg.tapped_date = form.tapped_date.data
        keg.tapped = form.tapped.data
        if id == "add":
            db.session.add(keg)
        db.session.commit()

    return render_template('keg.html',
            form=form,
            keg=keg)

@app.route('/keg/<id>/edit')
@auth.requires_auth
def edit_keg(id):
    return 'Hello World!'

@app.route('/beers')
def beers():
    '''Displays all beers'''
    return render_template('beers.html',
            beers=sorted(models.Beer.query.all(), key=lambda x: x.name,
                reverse=False))

@app.route('/beer/<id>', methods=['GET', 'POST'])
@auth.requires_auth
def beer(id):
    '''Displays a certain beer or the pace to create a beer'''
    form = BeerForm()
    if id == "add":
        beer = models.Beer()
    else:
        beer = models.Beer.query.get(id)
        if beer == None:
            return render_template('404.html'), 404
        elif request.method == "GET":
            form.abv.data = beer.abv
            form.ba_score.data = beer.ba_score
            form.brewer.data = beer.brewer
            form.isi_score.data = beer.isi_score
            form.link.data = beer.link
            form.name.data = beer.name
            form.style.data = beer.style


    if form.validate_on_submit():
        beer.name=form.name.data
        beer.style=form.style.data
        beer.brewer=form.brewer.data
        beer.abv=form.abv.data
        beer.ba_score=form.ba_score.data
        beer.isi_score=form.isi_score.data
        beer.link=form.link.data
        if id == "add":
            db.session.add(beer)
        db.session.commit()
        flash(beer)
    return render_template('beer.html',
            form=form,
            beer=beer)

@app.route('/beer/<id>/edit')
def edit_beer(id):
    return 'Hello World!'
