import bs4
import requests
import csv


def scrape_page(page_num):
    """
    function to scrape reviews from the below url and filter out all the reviews

    :param page_num: int - page number which is part of the url from where reviews have to be scraped

    :return: list - list of reviews
    """
    url = f'https://www.broadband.co.uk/broadband/providers/bt/reviews/page:{page_num}/#reviews'
    response = requests.get(url)
    # print(response.text)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    reviews_list = soup.findAll('div', class_='review__row')   # get each reviewer details and ratings
    # print(reviews_list)
    return reviews_list


def get_location(review):
    """
    function to extract the location of the particular review

    :param review: string - html code for the current review

    :return: string - location of the particular review
    """
    location = review.find('div', class_='review__location').dt.dd.text.strip()
    return location


def get_subject(review):
    """
    function to extract the subject of the particular review

    :param review: string - html code for the current review

    :return: string - subject of the particular review
    """
    subject = review.find('div', class_='review__subject').dd.text.strip()
    return subject


def get_date(review):
    """
    function to extract the published date of the particular review

    :param review: string - html code for the current review

    :return: string - published date of the particular review
    """
    date = review.find('div', class_='review__date').dd.text.strip()
    return date


def get_ratings(review):
    """
    function to extract the star ratings (numbered from 1 to 5) for different features (Satisfaction, Customer Service,
    Speed & Reliability) of the particular review

    :param review: string - html code for the current review

    :return: dictionary - ratings with above features and their ratings as key-value pairs
    """
    ratings = {'Satisfaction': '',
               'Customer Service': '',
               'Speed': '',
               'Reliability': ''
              }

    # get the list of ratings from the html data
    ratings_list = review.find('ul', class_='ratings')
    for item in ratings_list:
        if item.text.find('Satisfaction') != -1:
            ratings['Satisfaction'] = item.span.text

        elif item.text.find('Customer Service') != -1:
            ratings['Customer Service'] = item.span.text

        elif item.text.find('Speed') != -1:
            ratings['Speed'] = item.span.text

        elif item.text.find('Reliability') != -1:
            ratings['Reliability'] = item.span.text

    return ratings


def get_comment(review):
    """
    function to extract the comment of the particular review

    :param review: string - html code for the current review

    :return: string - comment of the particular review
    """
    review_block = review.find('div', class_='review__body')
    if review_block:
        comment = review_block.dd.text.strip()
    else:
        comment = ''
    return comment


def write_data_to_csv(locations, review_subjects, published_dates,
                      satisfaction, customer_service, speed, reliability, comments):
    """
    function to write the extracted data from the reviews into a csv file (reviews.csv)

    :param locations: list of locations in the same order as seen on the url (descending order by date)
    :param review_subjects: list of review subjects in the same order as seen on the url
    :param published_dates: list of published dates in the same order as seen on the url
    :param satisfaction: list of satisfaction ratings in the same order as seen on the url
    :param customer_service: list of customer service ratings in the same order as seen on the url
    :param speed: list of speed ratings in the same order as seen on the url
    :param reliability: list of reliability ratings in the same order as seen on the url
    :param comments: list of comments in the same order as seen on the url

    :return:
    """
    with open('reviews.csv', 'a') as file:
        csv_writer = csv.writer(file)
        header = ['Location', 'Review Subject', 'Review Date', 'Satisfaction',
                  'Customer Service', 'Speed', 'Reliability', 'Comments']
        csv_writer.writerow(header)
        # print(len(locations), len(review_subjects),len(published_dates), len(satisfaction),
        #       len(customer_service), len(speed), len(reliability), len(comments))
        for i in range(len(locations)):
            data = [locations[i], review_subjects[i], published_dates[i],
                    satisfaction[i], customer_service[i], speed[i], reliability[i], comments[i]]
            csv_writer.writerow(data)
