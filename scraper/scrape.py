from .service import MailService


def fetch_messages(service, uid, inbox_label):
    # This is to call gmail api to get messages in the inbox
    inbox_unread = service.list(userId=uid, labelIds=[inbox_label]).execute()
    # If you want to get only unread add one more label 'UNREAD' to the labelIds
    messages_info = inbox_unread['messages']
    return messages_info


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
    unique_addresses = []
    business_ids = []
    personal_ids = []
    for id in ids:
        if id not in unique_addresses:
            unique_addresses.append(id)
            if id[id.index('@') + 1:len(id) - 1] not in known_domains:
                business_ids.append(id)
            else:
                personal_ids.append(id)
    return business_ids, personal_ids


def write(file_name, ids):
    with open(file_name, 'w') as file:
        for id in ids:
            file.write("%s\n" % id)


def main(uid, cred_file_path, known_domains_path, out_business_ids_path, out_personal_ids_path):
    label = 'INBOX'
    known_domains = open(known_domains_path).read().splitlines()
    mail_service = MailService(cred_file_path)
    messages = fetch_messages(mail_service.get_service(), uid, label)
    ids = extract_ids(uid, mail_service.get_service(), messages)
    business_ids, personal_ids = classify(ids, known_domains)
    write(out_business_ids_path, business_ids)
    write(out_personal_ids_path, personal_ids)
