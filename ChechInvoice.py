#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass, poplib
Mailbox = poplib.POP3_SSL('', '995') 
Mailbox.user("") 
Mailbox.pass_("") 
