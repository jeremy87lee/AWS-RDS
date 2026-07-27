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
            g.flights.id if g.flights.id else "N/A",
            g.flights.departure_destination if g.flights.departure_destination else "N/A",
            g.flights.destination if g.flights.destination else "N/A",
            g.flights.plane.id if g.flights.plane.id else "N/A",
            g.flights.plane.model if g.flights.plane.model else "N/A",
            g.flights.plane.capacity if g.flights.plane.capacity else "N/A",
            g.flights.pilot.id if g.flights.pilot.id else "N/A",
            g.flights.pilot.name if g.flights.pilot.name else "N/A",
            g.flights.departure_time if g.flights.departure_time else "N/A",
            g.flights.arrival_time if g.flights.arrival_time else "N/A"
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