import csv
import datetime
import requests

def write_heading(file):
    file.write('''<!DOCTYPE html>
<html>
<head>
<style type="text/css">

@import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;900&display=swap');
* {
    margin: 0;
    border: 0;
    padding: 0;
}
body {
    font-family: 'Lato', sans-serif;
    background-color: #d8dbdb;
    font-size: 18px;
    max-width: 700px;
    margin: 0 auto;
    padding: 2%;
    color: #565859;
}
.wrapper {
    background: #f6faff;
    box-shadow: 0 0 10px #666;
}
img {
    max-width: 100%;
}
.logo {
    padding: 1% 0;
    text-align: center;
}
.logo img {
    max-width: 220px;
}
h1, h2 {
    letter-spacing: 1px;
    padding-bottom: 15px;
}
p {
    line-height: 28px;
    padding-bottom: 25px;
}
.button {
    background: #303840;
    color: #fff;
    text-decoration: none;
    font-weight: 800;
    padding: 10px 14px;
    border-radius: 8px;
    letter-spacing: 2px;
}
.one-col {
    padding: 20px 0 40px;
    text-align: center;
}
.line {
    clear: both;
    height: 1px;
    background-color: #303840;
    margin: 15px auto 10px;
    width: 98%;
}


.two-col h2 {
  text-align: center;
  font-family:'Courier New', Courier, monospace;
  color: rgb(118, 127, 135);
}
p {
  font-size: 18px;
  font-family: Arial, sans-serif;
  color: #333;
  text-align: center;
  background-color: #eee;
  border: 1px solid #ccc;
  padding: 10px;
}
h3 {
    text-align: center;
}

a {
  color: black;
}


table {
  border-collapse: collapse;
  width: 100%;
}

th, td {
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}
ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
}



li {
  display: block;
  margin-bottom: 10px;
  background-color: #f2f2f2;
  padding: 10px;
}

li:before {
  content:'⚫';
  font-size: 20px;
  color: #ff0000;
  margin-right: 10px;
}
</style>
</head>
<body>''')

def get_weather(file, city, name):
    now = datetime.datetime.now()
    date_string = now.strftime("%d, %B %Y")
    url = 'https://wttr.in/{}?format=3'.format(city)
    res = requests.get(url)

    file.write(f'''<div class="wrapper">
            <div class="banner">
            </div>
            <div class="one-col">
                <h1>Good Morning, {name}</h1>
                <p>Today is {date_string}, and the temperature is going to be around:
                <br>
                {res.text}
                </p>
            </div>''')

def generate_html_files_from_csv(csv_file):
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            city = row['City']
            name = row['Name']
            email = row['Email']
            file = open('{}.html'.format(name), 'w', encoding="utf-8")
            write_heading(file)
            get_weather(file, city=city, name=name)
            file.write('</body></html>')
            file.close()

# Example usage:
# generate_html_files_from_csv('contacts.csv')
