import logging

from config import WebConfig
from web.routes import app
from fastapi.middleware.cors import CORSMiddleware

import threading

from services.admin_service import AdminService
from persistence.token_dao import TokenDAO
from database import SessionLocal
from exceptions import TokenNotFoundException

logging.getLogger().setLevel(logging.INFO)

if WebConfig.CORS_ENABLED:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=WebConfig.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

dao = TokenDAO(SessionLocal())
admin_service = AdminService(dao)


def wait_for_input(name):
    while True:
        command = input()

        args = command.split()
        if not args:
            continue
        if len(args) != 2:
            print('Invalid number of arguments!\n')
            continue

        if args[0] == 'show':
            nick = args[1]
            active_tokens = admin_service.get_all_active(nick)

            for active_token in active_tokens:
                print(active_token)
            print()

        elif args[0] == 'revoke':
            try:
                token = args[1]
                admin_service.revoke(token)

                print(f'Token {token} is revoked!\n')
            except TokenNotFoundException:
                print('Token not found!\n')
        else:
            print(f'Unknown command {command}\n')


thread = threading.Thread(target=wait_for_input, args=(1,), daemon=True)
thread.start()
