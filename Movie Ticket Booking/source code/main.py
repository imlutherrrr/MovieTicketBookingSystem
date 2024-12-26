import os
from flask import Flask, request, render_template, session, redirect
import pymysql

app = Flask(__name__)
app.secret_key = "movie_ticket"
conn = pymysql.connect(host="localhost", user="root", password="Luther@1234", db="movie_ticket_booking")
cursor = conn.cursor()
admin_username = "admin"
admin_password = "admin"


APP_ROOT = os.path.dirname(__file__)
APP_ROOT = APP_ROOT + "/static"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")


@app.route("/admin_login1", methods=['post'])
def admin_login1():
    username = request.form.get("username")
    password = request.form.get("password")
    if admin_username == username and admin_password == password:
        session['role'] = 'admin'
        return redirect("/admin_home")
    return render_template("message2.html", message="Invalid Login Details")


@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")


@app.route("/add_locations")
def add_locations():
    return render_template("add_locations.html")


@app.route("/add_locations1", methods=['post'])
def add_locations1():
    name = request.form.get("name")
    cursor.execute("insert into location(location_name) values('" + str(name) + "')")
    conn.commit()
    return {"message": "Location Added Successfully"}


@app.route("/get_locations")
def get_locations():
    cursor.execute("select * from location")
    locations = cursor.fetchall()
    return render_template("view_locations.html", locations=locations)


@app.route("/add_theatres")
def add_theatres():
    cursor.execute("select * from location")
    locations = cursor.fetchall()
    return render_template("add_theatres.html", locations=locations)


@app.route("/add_theatres1", methods=['post'])
def add_theatres1():
    location_id = request.form.get("location_id")
    name = request.form.get("name")
    picture = request.files.get("picture")
    address = request.form.get("address")
    path = APP_ROOT + "/picture/" + picture.filename
    picture.save(path)
    cursor.execute("insert into theatre(name,picture,address,location_id) values('"+str(name)+"', '"+str(picture.filename)+"', '"+str(address)+"', '"+str(location_id)+"')")
    conn.commit()
    return render_template("message.html", message="Theatre added successfully")


@app.route("/view_theatres")
def view_theatres():
    cursor.execute("select * from theatre")
    theatres = cursor.fetchall()
    return render_template("view_theatres.html", theatres=theatres)


@app.route("/add_screens")
def add_screens():
    cursor.execute("select * from location")
    locations = cursor.fetchall()
    return render_template("add_screens.html", locations=locations)


@app.route("/get_theatre_options")
def get_theatre_options():
    location_id = request.args.get("location_id")
    cursor.execute("select * from theatre where location_id ='"+str(location_id)+"'")
    theatres = cursor.fetchall()
    return render_template("get_theatre_options.html", theatres=theatres)


@app.route("/add_screens1", methods=['post'])
def add_screens1():
    theatre_id = request.form.get("theatre_id")
    screen_title = request.form.get("screen_title")
    screen_size = request.form.get("screen_size")
    sound = request.form.get("sound")
    number_of_seats = request.form.get("number_of_seats")
    cursor.execute("insert into screen(number_of_seats,screen_size,sound,theatre_id,screen_title) values('"+str(number_of_seats)+"', '"+str(screen_size)+"', '"+str(sound)+"', '"+str(theatre_id)+"', '"+str(screen_title)+"')")
    conn.commit()
    return {"message": "Screen Added Successfully"}


@app.route("/get_screens")
def get_screens():
    cursor.execute("select * from screen")
    screens = cursor.fetchall()
    return render_template("view_screens.html", str=str, screens=screens, get_theatre_by_theatre_id=get_theatre_by_theatre_id, get_timings_by_screen_id=get_timings_by_screen_id)


def get_theatre_by_theatre_id(theatre_id):
    cursor.execute("select * from theatre where theatre_id ='"+str(theatre_id)+"'")
    theatre = cursor.fetchall()
    return theatre


def get_timings_by_screen_id(screen_id):
    cursor.execute("select * from timings where screen_id ='"+str(screen_id)+"'")
    timings = cursor.fetchall()
    return timings


@app.route("/add_timings")
def add_timings():
    screen_id = request.args.get("screen_id")
    show_time = request.args.get("show_time")
    count = cursor.execute("SELECT * from timings where TIMEDIFF('"+str(show_time)+"', show_time)<'03:00:00' and screen_id='"+str(screen_id)+"'")
    if count == 0:
        cursor.execute("insert into timings(screen_id,show_time) values('"+str(screen_id)+"', '"+str(show_time)+"')")
        conn.commit()
        return {"message": "Show Time Added"}
    else:
        return {"message": "Minimum duration is 3 hrs between two shows"}


@app.route("/add_movies")
def add_movies():
    return render_template("add_movies.html")


@app.route("/add_movies1", methods=['post'])
def add_movies1():
    movie_name = request.form.get("movie_name")
    picture = request.files.get("picture")
    duration = request.form.get("duration")
    genre = request.form.get("genre")
    description = request.form.get("description")
    status = 'coming soon'
    release_date = request.form.get("release_date")
    path = APP_ROOT + "/picture/" + picture.filename
    picture.save(path)
    count = cursor.execute("select * from movies where picture='"+str(picture.filename)+"' and description ='"+str(description)+"'")
    if count == 0:
        cursor.execute("insert into movies(movie_name,picture,duration,genre,description,status,release_date)values('"+str(movie_name)+"', '"+str(picture.filename)+"', '"+str(duration)+"', '"+str(genre)+"', '"+str(description)+"', '"+str(status)+"', '"+str(release_date)+"')")
        conn.commit()
        return render_template("message.html", message="Movie Added Successfully")
    return render_template("message2.html", message="Movie Already Exists")


@app.route("/view_movies")
def view_movies():
    return render_template("view_movies.html")


@app.route("/get_movies")
def get_movies():
    movie_name = request.args.get("movie_name")
    cursor.execute("select * from movies where movie_name like '%"+str(movie_name)+"%'")
    movies = cursor.fetchall()
    return render_template("get_movies.html", movies=movies)


@app.route("/assign_movies", methods=['post'])
def assign_movies():
    movies_id = request.form.get("movies_id")
    cursor.execute("select * from location")
    locations = cursor.fetchall()
    return render_template("assign_movies.html", movies_id=movies_id, locations=locations)


@app.route("/get_screen_options")
def get_screen_options():
    theatre_id = request.args.get("theatre_id")
    if theatre_id == None or theatre_id == "":
        query = "select * from theatre"
    else:
        query = "select * from theatre where theatre_id ='"+str(theatre_id)+"'"
    cursor.execute(query)
    theatres = cursor.fetchall()
    return render_template("get_screen_options.html", theatres=theatres, get_screens_by_theatre=get_screens_by_theatre)


def get_screens_by_theatre(theatre_id):
    cursor.execute("select * from screen where theatre_id ='"+str(theatre_id)+"'")
    screens = cursor.fetchall()
    return screens


@app.route("/assign_movies1", methods=['post'])
def assign_movies1():
    from_date = request.form.get("from_date")
    to_date = request.form.get("to_date")
    movies_id = request.form.get("movies_id")
    ticket_price = request.form.get("ticket_price")
    screen_ids = request.form.getlist("screen_ids")
    for screen_id in screen_ids:
        cursor.execute("insert into now_showing(from_date,to_date,screen_id,movies_id,ticket_price) values('"+str(from_date)+"', '"+str(to_date)+"', '"+str(screen_id)+"', '"+str(movies_id)+"','"+str(ticket_price)+"')")
        conn.commit()
    return render_template("message.html", message="Movie Assigned successfully")


@app.route("/now_showing")
def now_showing():
    return render_template("now_showing.html")


@app.route("/get_now_showing_movies")
def get_now_showing_movies():
    movie_name = request.args.get("movie_name")
    booking_date = request.args.get("booking_date")
    cursor.execute("select * from movies where movie_name like '%"+str(movie_name)+"%' and movies_id in (select movies_id from now_showing where ('"+str(booking_date)+"' between from_date and to_date) or from_date = '"+str(booking_date)+"' or to_date ='"+str(booking_date)+"')")
    movies = cursor.fetchall()
    return render_template("get_now_showing_movies.html", movies=movies, booking_date=booking_date)


@app.route("/now_showing_screens", methods=['post'])
def now_showing_screens():
    movies_id = request.form.get("movies_id")
    booking_date = request.form.get("booking_date")
    cursor.execute("select * from now_showing where movies_id = '"+str(movies_id)+"' and (('"+str(booking_date)+"' between from_date and to_date) or from_date='"+str(booking_date)+"' or to_date='"+str(booking_date)+"') ")
    now_showings = cursor.fetchall()
    theatre_ids = []
    for now_showing in now_showings:
        cursor.execute("select * from screen where screen_id ='"+str(now_showing[3])+"'")
        screens = cursor.fetchall()
        theatre_ids.append(screens[0][4])
    theatre_ids = set(theatre_ids)
    return render_template("now_showing_screens.html", theatre_ids=theatre_ids, booking_date=booking_date, movies_id=movies_id, get_shows_by_theatre_id=get_shows_by_theatre_id, get_screen_by_screen_id=get_screen_by_screen_id, get_timings_by_screen_id=get_timings_by_screen_id, str=str)


def get_shows_by_theatre_id(theatre_id,booking_date,movies_id):
    cursor.execute("select * from theatre where theatre_id ='"+str(theatre_id)+"'")
    theatres = cursor.fetchall()
    query = "select * from now_showing where movies_id = '"+str(movies_id)+"' and (('"+str(booking_date)+"' between from_date and to_date) or from_date='"+str(booking_date)+"' or to_date='"+str(booking_date)+"') and screen_id in (select screen_id from screen where theatre_id ='"+str(theatre_id)+"')"
    cursor.execute(query)
    now_showings = cursor.fetchall()
    return theatres[0], now_showings


def get_screen_by_screen_id(screen_id):
    cursor.execute("select * from screen where screen_id ='"+str(screen_id)+"'")
    screens = cursor.fetchall()
    return screens[0]


@app.route("/booking")
def booking():
    timing_id = request.args.get("timing_id")
    screen_id = request.args.get("screen_id")
    movies_id = request.args.get("movies_id")
    booking_date = request.args.get("booking_date")
    cursor.execute("select * from screen where screen_id = '"+str(screen_id)+"'")
    screen = cursor.fetchall()
    cursor.execute("select * from theatre where theatre_id in(select theatre_id from screen where screen_id ='"+str(screen_id)+"')")
    theatre = cursor.fetchall()
    cursor.execute("select * from movies where movies_id = '" + str(movies_id) + "'")
    movie = cursor.fetchall()
    cursor.execute("select * from timings where timings_id = '" + str(timing_id) + "'")
    timing = cursor.fetchall()
    cursor.execute("select * from now_showing where screen_id ='"+str(screen_id)+"'")
    now_showing = cursor.fetchall()
    return render_template("booking.html", str=str, int=int, now_showing=now_showing[0], screen=screen[0], movie=movie[0], timing=timing[0], theatre=theatre[0], booking_date=booking_date)


@app.route("/booking_action", methods=['post'])
def booking_action():
    user_id = session['user_id']
    now_showing_id = request.form.get("now_showing_id")
    cursor.execute("select * from now_showing where now_showing_id ='"+str(now_showing_id)+"'")
    now_showings = cursor.fetchall()
    now_showing = now_showings[0]
    timings_id = request.form.get("timings_id")
    cursor.execute("select * from timings where timings_id ='"+str(timings_id)+"'")
    timings = cursor.fetchall()
    timing = timings[0]
    theatre_id = request.form.get("theatre_id")
    cursor.execute("select * from theatre where theatre_id ='"+str(theatre_id)+"'")
    theatre = cursor.fetchall()
    booking_date = request.form.get("booking_date")
    screen_id = request.form.get("screen_id")
    cursor.execute("select * from screen where screen_id = '"+str(screen_id)+"'")
    screens = cursor.fetchall()
    screen = screens[0]
    cursor.execute("select * from movies where movies_id in(select movies_id from now_showing where now_showing_id = '"+str(now_showing_id)+"')")
    movies = cursor.fetchall()
    movie = movies[0]
    status = 'payment pending'
    selected_seats = []
    for i in range(1, int(screen[1])):
        selected_seat = request.form.get("seat_number" + str(i))
        if selected_seat is not None:
            selected_seats.append(selected_seat)
    number_of_seats = len(selected_seats)
    amount = int(number_of_seats) * int(now_showing[5])
    cursor.execute("insert into booking(user_id,timings_id,status,booking_date,number_of_seats,now_showing_id,amount) values('"+str(user_id)+"', '"+str(timings_id)+"', '"+str(status)+"', '"+str(booking_date)+"', '"+str(number_of_seats)+"', '"+str(now_showing_id)+"', '"+str(amount)+"')")
    conn.commit()
    booking_id = cursor.lastrowid
    for selected_seat in selected_seats:
        cursor.execute("insert into booked_seats(booking_id,seat_numbers,status) values('" + str(booking_id) + "','" + str(selected_seat) + "','" + str(status) + "')")
        conn.commit()
    return render_template("payment.html", booking_id=booking_id, selected_seats=selected_seats, screen=screen, movie=movie, now_showing=now_showing, booking_date=booking_date, amount=amount, theatre=theatre[0], timing=timing, str=str)


@app.route("/payment", methods=['post'])
def payment():
    booking_id = request.form.get("booking_id")
    card_number = request.form.get("card_number")
    card_holder_name = request.form.get("card_holder_name")
    cvv = request.form.get("cvv")
    expiry_date = request.form.get("expiry_date")
    cursor.execute("insert into payment(booking_id,card_number,card_holder_name,cvv,expiry_date) values('"+str(booking_id)+"', '"+str(card_number)+"', '"+str(card_holder_name)+"', '"+str(cvv)+"', '"+str(expiry_date)+"')")
    conn.commit()
    cursor.execute("update booking set status ='Ticket Booked' where booking_id ='"+str(booking_id)+"'")
    conn.commit()
    cursor.execute("update booked_seats set status ='Ticket Booked' where booking_id ='" + str(booking_id) + "'")
    conn.commit()
    return render_template("message.html", message="Ticket Booked Successfully")


@app.route("/view_bookings")
def view_bookings():
    query = ""
    if session['role'] == 'user':
        user_id = session['user_id']
        query = "select * from booking where user_id = '" + str(user_id) + "'"
    else:
        movies_id = request.args.get("movie_id")
        query = "select * from booking where now_showing_id in (select now_showing_id from now_showing where movies_id ='"+str(movies_id)+"')"
    cursor.execute(query)
    bookings = cursor.fetchall()
    return render_template("view_bookings.html", bookings=bookings, get_seat_numbers_by_booking_id=get_seat_numbers_by_booking_id, get_timings_by_now_showing_id=get_timings_by_now_showing_id, str=str, get_theatre_by_now_showing_id=get_theatre_by_now_showing_id, get_screen_by_now_showing_id=get_screen_by_now_showing_id, get_movies_by_now_showing_id=get_movies_by_now_showing_id)


def get_movies_by_now_showing_id(now_showing_id):
    cursor.execute("select * from movies where movies_id in(select movies_id from now_showing where now_showing_id ='"+str(now_showing_id)+"')")
    movies = cursor.fetchall()
    return movies[0]


def get_screen_by_now_showing_id(now_showing_id):
    cursor.execute("select * from screen where screen_id in(select screen_id from now_showing where now_showing_id ='"+str(now_showing_id)+"')")
    screens = cursor.fetchall()
    return screens[0]


def get_theatre_by_now_showing_id(now_showing_id):
    cursor.execute("select * from theatre where theatre_id in(select theatre_id from screen where screen_id in( select screen_id from now_showing where now_showing_id ='"+str(now_showing_id)+"'))")
    theatres = cursor.fetchall()
    return theatres[0]


def get_timings_by_now_showing_id(now_showing_id):
    cursor.execute("select * from timings where screen_id in(select screen_id from now_showing where now_showing_id ='"+str(now_showing_id)+"')")
    timings = cursor.fetchall()
    return timings[0]


def get_seat_numbers_by_booking_id(booking_id):
    cursor.execute("select * from booked_seats where booking_id ='"+str(booking_id)+"'")
    seat_numbers = cursor.fetchall()
    return seat_numbers


@app.route("/cancel_booking")
def cancel_booking():
    booking_id = request.args.get("booking_id")
    cursor.execute("update booking set status ='Ticket Cancelled' where booking_id ='"+str(booking_id)+"'")
    conn.commit()
    cursor.execute("update booked_seats set status ='Ticket Cancelled' where booking_id ='" + str(booking_id) + "'")
    conn.commit()
    return render_template("message.html", message="Ticket Cancelled Successfully")


@app.route("/user_registration")
def user_registration():
    return render_template("user_registration.html")


@app.route("/user_registration1", methods=['post'])
def user_registration1():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    count = cursor.execute("select * from user where email='"+str(email)+"' and phone='"+str(phone)+"'")
    if count == 0:
        cursor.execute("insert into user(name,email,phone,password) values('"+str(name)+"', '"+str(email)+"', '"+str(phone)+"', '"+str(password)+"')")
        conn.commit()
        return render_template("message.html", message="User Added Successfully")
    return render_template("message.html", message2="Email or Phone already exists")


@app.route("/user_login")
def user_login():
    return render_template("user_login.html")


@app.route("/user_login1", methods=['post'])
def user_login1():
    email = request.form.get("email")
    password = request.form.get("password")
    count = cursor.execute("select * from user where email='"+str(email)+"' and password='"+str(password)+"'")
    if count > 0:
        user = cursor.fetchall()
        session['user_id'] = user[0][0]
        session['role'] = 'user'
        return redirect("/user_home")
    return render_template("message.html", message2="Invalid Login Details")


@app.route("/user_home")
def user_home():
    return render_template("user_home.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


app.run(debug=True)
