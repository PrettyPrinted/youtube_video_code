from imap_tools import MailBox

MAIL_PASSWORD = "password"
MAIL_USERNAME = "email@email.com"

with MailBox("imap.fastmail.com").login(MAIL_USERNAME, MAIL_PASSWORD, "Inbox") as mb:
    #print(mb.folder.list())
    #print(mb.folder.get())
    for msg in mb.fetch(limit=5, reverse=True, mark_seen=False):
        print(msg.subject, msg.date, msg.flags, msg.text, msg.uid)

    mb.move("123", "Drafts")
