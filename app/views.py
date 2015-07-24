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
    if request.method == "GET":
        form.kegerators.data = floor.kegerators
        form.number.data = floor.number
    if form.validate_on_submit():
        floor.number = form.number.data
        floor.kegerators = form.kegerators.data
        db.session.commit()
    return render_template('floor.html',
            floor = floor,
            form = form)

@app.route('/floor/add', methods=['GET', 'POST'])
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
        new_floor.kegerators = form.kegerators.data
        new_floor.number = form.number.data
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
    '''Displays a certain kegerator'''
    kegerator = models.Kegerator.query.get_or_404(id)
    form = KegeratorForm()
    floors = models.Floor.query.all()
    form.floor_id.choices = [(f.id, f.__repr__()) for f in floors]
    kegs = models.Keg.query.all()
    form.kegs.choices = [(k.id, k.__repr__()) for k in kegs]
    # Fill out form
    if request.method == "GET":
        form.clean_date.data = kegerator.clean_date
        form.co2.data = kegerator.co2
        form.co2_date.data = kegerator.co2_date
        form.floor_id.data = kegerator.floor_id
        form.kegs.data = kegerator.kegs
        form.name.data = kegerator.name
    # Update model
    if form.validate_on_submit():
        kegerator.clean_date = form.clean_date.data
        kegerator.co2_date = form.co2_date.data
        kegerator.co2 = form.co2.data
        kegerator.floor_id = form.floor_id.data
        kegerator.kegs = form.kegs.data
        kegerator.name = form.name.data
        db.session.commit()
    return render_template('kegerator.html',
            kegerator = kegerator,
            form = form)

@app.route('/kegerator/add', methods=['GET','POST'])
@auth.requires_auth
def add_kegerator():
    # Create the form
    form = KegeratorForm()
    floors = models.Floor.query.all()
    form.floor_id.choices = [(f.id, f.__repr__()) for f in floors]
    kegs = models.Keg.query.all()
    form.kegs.choices = [(k.id, k.__repr__()) for k in kegs]
    # Create the kegerator
    new_kegerator = models.Kegerator()
    if form.validate_on_submit():
        new_kegerator.clean_date = form.clean_date.data
        new_kegerator.co2_date = form.co2_date.data
        new_kegerator.co2 = form.co2.data
        new_kegerator.floor_id = form.floor_id.data
        new_kegerator.kegs = form.kegs.data
        new_kegerator.name = form.name.data
        db.session.add(new_kegerator)
        db.session.commit()
        return redirect("/kegerator/{0}".format(new_kegerator.id), 302)
    return render_template('kegerator_add.html',
            form=form)

@app.route('/kegs')
def kegs():
    '''Displays all kegs'''
    return render_template('kegs.html',
            kegs=sorted(models.Keg.query.all(), key=lambda x: x.beer.name,
                reverse=False))

@app.route('/keg/<id>', methods=['GET', 'POST'])
@auth.requires_auth
def keg(id):
    '''Views particular keg'''
    keg = models.Keg.query.get_or_404(id)
    form = KegForm()
    beers = models.Beer.query.all()
    form.beer_id.choices = [(b.id, b.__repr__()) for b in beers]
    kegerators = models.Kegerator.query.all()
    form.kegerator_id.choices = [(k.id, k.__repr__()) for k in kegerators]
    # Fill out form
    if request.method == "GET":
        form.beer_id.data = keg.beer_id
        form.kegerator_id.data = keg.kegerator_id
        form.chilled.data = keg.chilled
        form.chilled_date.data = keg.chilled_date
        form.empty_date.data = keg.empty_date
        form.filled.data = keg.filled
        form.stocked.data = keg.stocked
        form.stocked_date.data = keg.stocked_date
        form.tapped.data = keg.tapped
        form.tapped_date.data = keg.tapped_date
    # Update model
    if form.validate_on_submit():
        keg.beer_id = form.beer_id.data
        keg.kegerator_id = form.kegerator_id.data
        keg.chilled_date = form.chilled_date.data
        keg.chilled = form.chilled.data
        keg.empty_date = form.empty_date.data
        keg.filled = form.filled.data
        keg.stocked_date = form.stocked_date.data
        keg.stocked = form.stocked.data
        keg.tapped_date = form.tapped_date.data
        keg.tapped = form.tapped.data
        db.session.commit()
    return render_template('keg.html',
            form=form,
            keg=keg)

@app.route('/keg/add', methods=['GET', 'POST'])
@auth.requires_auth
def add_keg():
    # Create the form
    form = KegForm()
    beers = models.Beer.query.all()
    form.beer_id.choices = [(b.id, b.__repr__()) for b in beers]
    kegerators = models.Kegerator.query.all()
    form.kegerator_id.choices = [(k.id, k.__repr__()) for k in kegerators]
    # Create the keg
    new_keg = models.Keg()
    if form.validate_on_submit():
        new_keg.beer_id = form.beer_id.data
        new_keg.kegerator_id = form.kegerator_id.data
        new_keg.chilled_date = form.chilled_date.data
        new_keg.chilled = form.chilled.data
        new_keg.empty_date = form.empty_date.data
        new_keg.filled = form.filled.data
        new_keg.stocked_date = form.stocked_date.data
        new_keg.stocked = form.stocked.data
        new_keg.tapped_date = form.tapped_date.data
        new_keg.tapped = form.tapped.data
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
@auth.requires_auth
def beer(id):
    '''Displays a certain beer or the pace to create a beer'''
    beer = models.Beer.query.get_or_404(id)
    form = BeerForm()
    kegs = models.Keg.query.all()
    form.kegs.choices = [(k.id, k.__repr__()) for k in kegs]
    # fill out form
    if request.method == "GET":
        form.abv.data = beer.abv
        form.ba_score.data = beer.ba_score
        form.brewer.data = beer.brewer
        form.isi_score.data = beer.isi_score
        form.kegs.data = beer.kegs
        form.link.data = beer.link
        form.name.data = beer.name
        form.style.data = beer.style
    if form.validate_on_submit():
        beer.abv = form.abv.data
        beer.ba_score = form.ba_score.data
        beer.brewer = form.brewer.data
        beer.isi_score = form.isi_score.data
        beer.kegs = form.kegs.data
        beer.link = form.link.data
        beer.name = form.name.data
        beer.style = form.style.data
        db.session.commit()
    return render_template('beer.html',
            form=form,
            beer=beer)

@app.route('/beer/add', methods=['GET', 'POST'])
@auth.requires_auth
def edit_beer(id):
    form = BeerForm()
    kegs = models.Keg.query.all()
    form.kegs.choices = [(k.id, k.__repr__()) for k in kegs]
    # create the beer
    new_beer - models.Beer()
    if form.validate_on_submit():
        new_beer.abv = form.abv.data
        new_beer.ba_score = form.ba_score.data
        new_beer.brewer = form.brewer.data
        new_beer.isi_score = form.isi_score.data
        new_beer.kegs = form.kegs.data
        new_beer.link = form.link.data
        new_beer.name = form.name.data
        new_beer.style = form.style.data
        db.session.add(new_beer)
        db.session.commit()
        return redirect("/floor/{0}".format(new_beer.id), 302)
    return render_template('beer_add.html',
            form=form)

