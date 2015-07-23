from app import db

class Floor(db.Model):
    '''Top level model contains a relationship to a kegerator and its number'''
    id = db.Column(db.Integer, primary_key=True)
    kegerators = db.relationship("Kegerator", backref="floor")
    number = db.Column(db.Integer, index=True, unique=True, default=0)

    def __repr__(self):
        if self.number:
            s = ['st','nd','rd','th']
            suffix = s[0]
            if self.number > 3:
                suffix = s[3]
            else:
                suffix = s[self.number-1]
            return "{0}{1}".format(self.number, suffix)
        return "None"

class Kegerator(db.Model):
    '''Has a relationship to the keg it contains and the floor it is on, there
    are columns that are not used yet'''
    id = db.Column(db.Integer, primary_key=True)
    # Info
    co2 = db.Column(db.Boolean)
    name = db.Column(db.String(32), unique=True)
    # Dates
    clean_date = db.Column(db.Date)
    co2_date = db.Column(db.Date)
    # Relationships
    floor_id = db.Column(db.Integer, db.ForeignKey('floor.id'))
    keg_id = db.Column(db.Integer, db.ForeignKey('keg.id'))

    def __repr__(self):
        return '{0}'.format(self.name)

class Keg(db.Model):
    '''Keg has a foreign_key relationship to a beer and general information
    about the keg'''
    id = db.Column(db.Integer, primary_key=True)
    # Relationships
    beer_id  = db.Column(db.Integer, db.ForeignKey('beer.id'))
    kegerator = db.relationship('Kegerator', backref='keg')
    # Info
    chilled = db.Column(db.Boolean)
    filled = db.Column(db.Integer)
    stocked = db.Column(db.Boolean)
    tapped = db.Column(db.Boolean)
    # Dates
    chilled_date = db.Column(db.Date)
    empty_date = db.Column(db.Date)
    filled_date = db.Column(db.Date)
    stocked_date = db.Column(db.Date)
    tapped_date = db.Column(db.Date)

    def __repr__(self):
        cold = "Warm"
        full = "Empty"
        if self.chilled:
            cold = "Cold"
        if self.filled:
            full = "Full"
        if self.beer_id:
            beer = Beer.query.get(self.beer_id)
            return '{0} {1} | {2}, {3}'.format(beer.name, beer.style, full,
                cold)
        return 'None | {0}, {1}'.format(full,cold)

class Beer(db.Model):
    '''Most basic model. Has a backwards relationship to the keg it is in'''
    id = db.Column(db.Integer, primary_key=True)
    # beer info
    abv = db.Column(db.Float(precision=4))
    brewer = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), index=True)
    style = db.Column(db.String(64), index=True)
    # misc
    ba_score = db.Column(db.Integer)
    keg = db.relationship('Keg', backref='beer')
    link = db.Column(db.String(128), unique=True)
    # voting
    isi_score = db.Column(db.Integer)
    votes = db.Column(db.Integer)

    def __repr__(self):
        return "{0} {1} | {2}".format(self.name, self.style, self.brewer)
