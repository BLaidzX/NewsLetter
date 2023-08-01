from combine_send import send_news_briefs
from heading import generate_html_files_from_csv
from main import write_body

write_body()
generate_html_files_from_csv('contacts.csv')
send_news_briefs('contacts.csv')