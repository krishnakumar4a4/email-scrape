from .service import MailService


def fetch_messages(service, uid, inbox_label):
    messages = []
    # This is to call gmail api to get messages in the inbox
    response = service.list(userId=uid, labelIds=[inbox_label]).execute()
    if 'messages' in response:
        messages.extend(response['messages'])

    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.list(userId=uid, labelIds=[inbox_label],
                                                   pageToken=page_token).execute()
        messages.extend(response['messages'])
    return messages


def extract_ids(uid, service, messages):
    headers_list = map(lambda msg: service.get(userId=uid, id=msg['id']).execute()['payload']['headers'],
                       messages)
    ids = []
    for headers in headers_list:
        from_header = list(filter(lambda hdr: hdr['name'] == 'From', headers))
        # date_header = list(filter(lambda hdr: hdr['name'] == 'Date', headers))
        val = from_header[0]['value']
        ids.append(val)
    return ids


def classify(ids, known_domains):
    unique_addresses = set()
    business_ids = []
    personal_ids = []
    for id in ids:
        unique_addresses.add(id)
        if id[id.index('@') + 1:len(id) - 1] not in known_domains:
            business_ids.append(id)
        else:
            personal_ids.append(id)
    return business_ids, personal_ids


def write(file_name, ids):
    print("started writing to ",file_name)
    with open(file_name, 'w') as file:
        for id in ids:
            file.write("%s\n" % id)
    file.close()


def main(uid, cred_file_path, known_domains_path, out_business_ids_path, out_personal_ids_path):
    label = 'INBOX'
    known_domains = open(known_domains_path).read().splitlines()
    mail_service = MailService(cred_file_path)
    do(known_domains, label, mail_service, out_business_ids_path, out_personal_ids_path, uid)


def do(known_domains, label, mail_service, out_business_ids_path, out_personal_ids_path, uid):
    messages = fetch_messages(mail_service.get_service(), uid, label)
    print("started getting email ids")
    ids = extract_ids(uid, mail_service.get_service(), messages)
    print("started classification")
    business_ids, personal_ids = classify(ids, known_domains)
    write(out_business_ids_path, business_ids)
    write(out_personal_ids_path, personal_ids)
