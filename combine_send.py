import csv
import smtplib
from email.message import EmailMessage


def stitch_files(headingfile, contentfile, output_path):
    with open(headingfile, 'r', encoding='utf-8') as file1:
        content1 = file1.read()

    with open(contentfile, 'r', encoding='utf-8') as file2:
        content2 = file2.read()

    combined_content = content1 + content2

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(combined_content)


def send_mail(recipient, content):
    message = EmailMessage()
    message["From"] = "newsbriefnoreply@gmail.com"
    message["To"] = recipient
    message["Subject"] = 'The news'

    message.set_content(content, 'html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login("newsbriefnoreply@gmail.com", "nykhxnxpxlqysybg")
        server.send_message(message)


def send_news_briefs(csv_file):
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            city = row['City']
            name = row['Name']
            email = row['Email']

            file1_path = '{}.html'.format(name)
            file2_path = 'output.html'
            output_path = '{}.html'.format(email)
            stitch_files(file1_path, file2_path, output_path)

            with open(output_path, 'r', encoding='utf-8') as file:
                email_content = file.read()

            send_mail(recipient=email, content=email_content)


# Example usage:
# send_news_briefs('contacts.csv')
