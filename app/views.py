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
    form = FloorForm(obj=floor)
    kegerators = models.Kegerator.query.all()
    form.kegerators.choices = [(k.id, k.__repr__()) for k in kegerators]
    form.kegerators.choices.insert(0, (0, ''))
    if form.validate_on_submit():
        form.populate_obj(floor)
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
    form.kegerators.choices = [(k, k.__repr__()) for k in kegerators]
    form.kegerators.choices.insert(0, (0, ''))
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
@auth.requires_auth
def kegerator(id):
    '''Displays a certain kegerator'''
    kegerator = models.Kegerator.query.get_or_404(id)
    form = KegeratorForm(obj=kegerator)
    floors = models.Floor.query.all()
    kegs = models.Keg.query.all()
    form.kegs.choices = [(k.id, k.__repr__()) for k in kegs]
    form.kegs.choices.insert(0, (0, ''))
    form.floor_id.choices = [(f.id, f.__repr__()) for f in floors]
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
def add_kegerator():
    # Create the form
    form = KegeratorForm()
    floors = models.Floor.query.all()
    form.floor_id.choices = [(f.id, f.__repr__()) for f in floors]
    form.floor_id.choices.insert(0, (0, ''))
    kegs = models.Keg.query.all()
    form.kegs.choices = [(k.id, k.__repr__()) for k in kegs]
    form.kegs.choices.insert(0, (0, ''))
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
@auth.requires_auth
def keg(id):
    '''Views particular keg'''
    keg = models.Keg.query.get_or_404(id)
    form = KegForm(obj=keg)
    beers = models.Beer.query.all()
    kegerators = models.Kegerator.query.all()
    form.beer_id.choices = [(b.id, b.__repr__()) for b in beers]
    form.beer_id.choices.insert(0, (0, ''))
    form.kegerator_id.choices = [(k.id, k.__repr__()) for k in kegerators]
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
def add_keg():
    # Create the form
    form = KegForm()
    beers = models.Beer.query.all()
    form.beer_id.choices = [(b.id, b.__repr__()) for b in beers]
    form.beer_id.choices.insert(0, (0, ''))
    kegerators = models.Kegerator.query.all()
    form.kegerator_id.choices = [(k.id, k.__repr__()) for k in kegerators]
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
@auth.requires_auth
def beer(id):
    '''Displays a certain beer or the pace to create a beer'''
    beer = models.Beer.query.get_or_404(id)
    form = BeerForm(obj=beer)
    kegs = models.Keg.query.all()
    form.kegs.choices = [(k.id, k.__repr__()) for k in kegs]
    form.kegs.choices.insert(0, (0, ''))
    if form.validate_on_submit():
        form.populate_obj(beer)
        db.session.commit()
    return render_template('beer.html',
            form=form,
            beer=beer)

@app.route('/beer/add', methods=['GET', 'POST'])
@auth.requires_auth
def edit_beer():
    form = BeerForm()
    kegs = models.Keg.query.all()
    form.kegs.choices = [(k.id, k.__repr__()) for k in kegs]
    form.kegs.choices.insert(0, (0, ''))
    # create the beer
    new_beer = models.Beer()
    if form.validate_on_submit():
        form.populate_obj(new_beer)
        db.session.add(new_beer)
        db.session.commit()
        return redirect("/beer/{0}".format(new_beer.id), 302)
    return render_template('beer_add.html',
            form=form)

