#!/usr/bin/env python
import argparse
from scraper.scrape import main

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape emails')
    parser.add_argument('-id', type=str, help='user id', default='me')
    parser.add_argument('-cred_file', type=str, help='credentials for api access', default="./resources/credentials.json")
    parser.add_argument('-known_domains_path', type=str,
                        help='path for the file with known domains', default="./resources/domains.txt")
    parser.add_argument('-business_ids_path', type=str,
                        help='file path to store business email ids', default="./resources/business.csv")
    parser.add_argument('-personal_ids_path', type=str,
                        help='file path to store personal email ids', default="./resources/personal.csv")
    args = parser.parse_args()
    main(args.id, args.cred_file, args.known_domains_path, args.business_ids_path, args.personal_ids_path)