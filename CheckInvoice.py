#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass, poplib
Mailbox = poplib.POP3_SSL('', '995') 
Mailbox.user("") 
Mailbox.pass_("") 
# detach.py -H imap.example.com -u user -p password  -f ~/tmp/attachments/{year}/{from}/{name} -v 'attached'
# detach.py -H imap.example.com -u user -p password  -f ~/tmp/attachments/{year}/{from}/{name.subject_section}&nbsp; -v --threads 5 'attached'


# http://zderadicka.eu/download-email-attachments-automagically/

# pip3 install -e https://github.com/izderadicka/imap_detach
