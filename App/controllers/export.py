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
    flights = Flight.query.all()
    gates_2 = []
    wb = Workbook()
    ws = wb.active
    ws.title = "Flights"
    
    ws.append([
        "Flight ID", "Departure Destination", "Destination", "Plane ID", "Plane Model",
        "Plane Capacity", "Pilot ID", "Pilot Name", "Departure Time", "Arrival Time", "Gate ID", "Gate Terminal"
    ])
    
    

    # Data rows
    for f in flights:
        
        for g in gates:
            if g.flight == f.id:
                gates_2.append(g)
        
        if gates_2:
            for g in gates_2:   
                ws.append([
                    f.id if g.flights else "N/A",
                    f.departure_destination if g.flights else "N/A",
                    f.destination if g.flights else "N/A",
                    f.plane.id if g.flights else "N/A",
                    f.plane.model if g.flights else "N/A",
                    f.plane.capacity if g.flights else "N/A",
                    f.pilot.id if g.flights else "N/A",
                    f.pilot.name if g.flights else "N/A",
                    f.departure_time if g.flights else "N/A",
                    f.arrival_time if g.flights else "N/A",
                    g.id if g.id else "N/A",
                    g.terminal if g.terminal else "N/A"
                ]) 
                gates_2.remove(g)
        else:
            ws.append([
                                f.id if g.flights else "N/A",
                                f.departure_destination if g.flights else "N/A",
                                f.destination if g.flights else "N/A",
                                f.plane.id if g.flights else "N/A",
                                f.plane.model if g.flights else "N/A",
                                f.plane.capacity if g.flights else "N/A",
                                f.pilot.id if g.flights else "N/A",
                                f.pilot.name if g.flights else "N/A",
                                f.departure_time if g.flights else "N/A",
                                f.arrival_time if g.flights else "N/A",
                                "N/A",
                                "N/A"
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