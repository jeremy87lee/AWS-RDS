from App.database import db
from App.models.flights import Flight

class Gate(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    terminal = db.Column(db.String(10), nullable=False)
    flight = db.Column(db.Integer,db.ForeignKey('flight.id'),nullable=False)
    
    def get_json(self):
        return {
            'id': self.id,
            'terminal': self.terminal,
            'flight': self.flight
        }