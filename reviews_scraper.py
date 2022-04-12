# a review on the page will always have reviewer details (location, subject & date) but may or many not have
# ratings or comments

from scraping_functions import scrape_page, get_location, get_subject, get_date, \
                               get_ratings, get_comment, write_data_to_csv


def get_location_add_to_list(review, locations):
    """
    function to get the location of the review and append it to the list of locations

    :param review: string - html code
    :param locations: list - list of locations
    """
    location = get_location(review)
    locations.append(location)


def get_subject_add_to_list(review, review_subjects):
    """
    function to get the subject of the review and append it to the list of subjects

    :param review: string - html code
    :param review_subjects: list - list of review subjects
    """
    subject = get_subject(review)
    review_subjects.append(subject)


def get_date_add_to_list(review, published_dates):
    """
    function to get the published date of the review and append it to the list of dates

    :param review: string - html code
    :param published_dates: list - list of published dates
    """
    date = get_date(review)
    published_dates.append(date)


def add_ratings_to_list(satisfaction, customer_service, speed, reliability, ratings):
    """
    function to add the star ratings (numbers from 1 to 5) in their respective lists

    :param satisfaction: list of satisfaction ratings
    :param customer_service: list of customer service ratings
    :param speed: list of speed ratings
    :param reliability: list of reliability ratings
    :param ratings: dictionary - ratings with above features and their ratings as key-value pairs
    """
    satisfaction.append(ratings['Satisfaction'])
    customer_service.append(ratings['Customer Service'])
    speed.append(ratings['Speed'])
    reliability.append(ratings['Reliability'])


def get_comment_add_to_list(review, comments):
    """
    function to get the comment of the review and append it to the list of comments

    :param review: string - html code
    :param comments: list - list of comments
    """
    comment = get_comment(review)
    comments.append(comment)


def main():
    # initialisation of page variables for the url
    page_num = 1
    # total_pages = 82
    total_pages = 2  # for testing

    # initialising list variables
    # the details from reviews will be extracted and appended to the respective lists defined below
    locations = []
    review_subjects = []
    published_dates = []
    satisfaction = []
    customer_service = []
    speed = []
    reliability = []
    comments = []

    while page_num < total_pages:
        reviews_list = scrape_page(page_num)

        for review in reviews_list:
            # a review can have either reviewer details or reviewer ratings or only comments as its child block
            review_block = list(review.children)[1]

            # in case of child being reviewer details, get the location, review subject & published date and append them
            # to their respective lists
            if review_block.name == 'div' and review_block.get('class')[0] == 'review__author':
                get_location_add_to_list(review, locations)
                get_subject_add_to_list(review, review_subjects)
                get_date_add_to_list(review, published_dates)

            
            # in case of child being 'review ratings', get the satisfaction, customer service, speed & reliability stars
            # and also get the comments
            elif review_block.name == 'div' and review_block.get('class')[0] == 'review__ratings':
                ratings = get_ratings(review)
                add_ratings_to_list(satisfaction, customer_service, speed, reliability, ratings)
                get_comment_add_to_list(review, comments)

            # in case of child being 'review no ratings', put the satisfaction, customer service, speed & reliability
            # ratings as blank and get the comments
            elif review_block.name == 'div' and review_block.get('class')[1] == 'review__noratings':
                ratings = {'Satisfaction': '',
                           'Customer Service': '',
                           'Speed': '',
                           'Reliability': ''
                           }
                add_ratings_to_list(satisfaction, customer_service, speed, reliability, ratings)
                get_comment_add_to_list(review, comments)

        page_num = page_num + 1  # increment the page number

    # write the extracted data to a csv file
    write_data_to_csv(locations, review_subjects, published_dates, satisfaction,
                      customer_service, speed, reliability, comments)


if __name__ == '__main__':
    main()
