#!/bin/sh
if [ ! -f vuln.db ]; then
  ADMIN_PW=$(python3 -c "import os;print(os.urandom(16).hex())")
  sqlite3 vuln.db <<EOF
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE,
  password TEXT
);
INSERT INTO users (username,password) VALUES ('guest','guest');
INSERT INTO users (username,password) VALUES ('admin','$ADMIN_PW');
EOF
fi
exec python3 src/app.py
