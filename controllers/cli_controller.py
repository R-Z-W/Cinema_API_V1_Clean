import click
from flask import current_app
from flask import Blueprint
from init import db, bcrypt
from models.movie import Movie
from models.theater import Theater
from models.customer import Customer
from models.employee import Employee
from models.invoice import Invoice
from models.showtime import Showtime
from models.ticket import Ticket

db_commands = Blueprint('db', __name__)


@db_commands.cli.command('create')
def create_tables():
    """Create the database tables."""
    db.create_all()
    print("Tables Created")

@db_commands.cli.command('drop')
def drop_tables():
    """Drop the database tables."""
    db.drop_all()
    print("Tables Dropped")

@db_commands.cli.command('seed')
def seed_tables():
    """Seeding Database"""
    with current_app.app_context():
        movies = [
            {
                'title': 'Inception',
                'year': 2010,
                'runtime': '148',
                'genre': 'Action',
                'director': 'Christopher Nolan',
                'plot': 'A thief with the rare ability to enter people\'s dreams and steal their secrets from their subconscious is given a final task that requires him to do the impossible: inception.',
                'language': 'English',
                'rating': 8.8
            },
            {
                'title': 'The Matrix',
                'year': 1999,
                'runtime': '136',
                'genre': 'Science Fiction',
                'director': 'Lana Wachowski, Lilly Wachowski',
                'plot': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
                'language': 'English',
                'rating': 8.7
            },
            {
                'title': 'The Godfather',
                'year': 1972,
                'runtime': '175',
                'genre': 'Crime',
                'director': 'Francis Ford Coppola',
                'plot': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
                'language': 'English',
                'rating': 9.2
            }
        ]

        theaters = [
            {
                'name': 'Cinema 1',
                'location': '1'
            },
            {
                'name': 'Cinema 3',
                'location': '3'
            },
            {
                'name': 'Cinema 5',
                'location': '5'
            }
        ]

        customers = [
            {
                'fname': 'John',
                'lname': 'Doe',
                #'password': 'abcd1234',
                'dob': '1985-06-15',
                'email': 'john.doe@example.com',
                'phone': '555-1234',
                'date_created': '2024-07-20'
            },
            {
                'fname': 'Jane',
                'lname': 'Smith',
                #'password': 'abcd1234',
                'dob': '1990-02-25',
                'email': 'jane.smith@example.com',
                'phone': '555-5678',
                'date_created': '2024-07-21'
            }
        ]

        employees = [
            {
                'fname': 'Alice',
                'lname': 'Johnson',
                'password': 'abcd1234',
                'dob': '1980-11-10',
                'email': 'alice.johnson@example.com',
                'phone': '555-8765',
                'role': 'Manager',
                'department': 'Management',
                'salary': 75000,
                'leave': 15,
                'leave_sick': 5,
                'date_created': '2024-07-20'
            },
            {
                'fname': 'Bob',
                'lname': 'Brown',
                'password': 'abcd1234',
                'dob': '1992-08-22',
                'email': 'bob.brown@example.com',
                'phone': '555-4321',
                'role': 'Staff',
                'department': 'Customer Service',
                'salary': 40000,
                'leave': 10,
                'leave_sick': 3,
                'date_created': '2024-07-21'
            }
        ]

        invoices = [
            {
                'total_price': 30.00,
                'status': 'Paid',
                'date_created': '2024-07-20',
                'date_delivered': '2024-07-20',
                'customer_id': 1,
                'employee_id': 1
            },
            {
                'total_price': 45.00,
                'status': 'Pending',
                'date_created': '2024-07-21',
                'date_delivered': None,
                'customer_id': 2,
                'employee_id': 2
            }
        ]

        showtimes = [
            {
                'start_time': '2024-07-20 19:00:00',
                'end_time': '2024-07-20 21:30:00',
                'date_created': '2024-07-10',
                'theater_id': 1,
                'movie_id': 1
            },
            {
                'start_time': '2024-07-21 20:00:00',
                'end_time': '2024-07-21 22:30:00',
                'date_created': '2024-07-11',
                'theater_id': 2,
                'movie_id': 2
            }
        ]

        tickets = [
            {
                'price': 15.00,
                'seat_number': 'A1',
                'date_created': '2024-07-20',
                'showtime_id': 1,
                'invoice_id': 1
            },
            {
                'price': 15.00,
                'seat_number': 'A2',
                'date_created': '2024-07-21',
                'showtime_id': 2,
                'invoice_id': 2
            }
        ]

        # Add Movies
        for movie_data in movies:
            movie = Movie(**movie_data)
            db.session.add(movie)
        
        # Add Theaters
        for theater_data in theaters:
            theater = Theater(**theater_data)
            db.session.add(theater)

        # Add Customers
        for customer_data in customers:
            customer = Customer(**customer_data)
            db.session.add(customer)

        # Add Employees
        for employee_data in employees:
            employee_data['password'] = bcrypt.generate_password_hash(employee_data['password']).decode('utf-8')
            employee = Employee(**employee_data)
            db.session.add(employee)

        # # Add Invoices
        for invoice_data in invoices:
            invoice = Invoice(**invoice_data)
            db.session.add(invoice)

        # Add Showtimes
        for showtime_data in showtimes:
            showtime = Showtime(**showtime_data)
            db.session.add(showtime)

        # Add Tickets
        for ticket_data in tickets:
            ticket = Ticket(**ticket_data)
            db.session.add(ticket)

        # Commit all changes
        db.session.commit()
        print("Tables Seeded")