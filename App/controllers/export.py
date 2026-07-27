from App.models import User
from App.database import db
from App.models.Gates import Gate
from App.models.Planes import Plane
from App.models.admin import Admin
from App.models.flights import Flight
from App.models.pilots import Pilot
from datetime import datetime
import pandas as pd
from flask import send_file
from openpyxl import Workbook
from io import BytesIO

def export_excel():
    gates = Gate.query.all()
    wb = Workbook()
    ws = wb.active
    ws.title = "Flights"
    
    ws.append([
        "Gate ID", "Terminal", "Flight ID", "Departure Destination", "Destination", "Plane ID", "Plane Model",
        "Plane Capacity", "Pilot ID", "Pilot Name", "Departure Time", "Arrival Time"
    ])

    # Data rows
    for g in gates:
        ws.append([
            g.id,
            g.terminal,
            g.flights.id,
            g.flights.departure_destination,
            g.flights.destination,
            g.flights.plane.id,
            g.flights.plane.model,
            g.flights.plane.capacity,
            g.flights.pilot.id,
            g.flights.pilot.name,
            g.flights.departure_time,
            g.flights.arrival_time
        ]) 
        
    # Save to an in-memory buffer instead of disk
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="flights.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )