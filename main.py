import reddit_service as reddit_service
import google_sheets_service as google_sheets_service


def main():
    extracted_posts_list = reddit_service.extract_posts_data()
    transformed_posts_list = reddit_service.transform_posts(extracted_posts_list)
    print(transformed_posts_list)
    google_sheets_service.upload(transformed_posts_list)


if __name__ == '__main__':
    main()
