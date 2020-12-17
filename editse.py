from datetime import datetime
import random
import os
import csv
import sqlite3


def main():
    running = True
    conn = sqlite3.connect('artificialStock.db', check_same_thread=False)
    c = conn.cursor()

    while running == True:
        cmd = input("Enter command: ")

        if cmd == 'delete':
            c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            print(c.fetchall())
            deletedTable = input("Enter table name to delete: ")
            try:
                c.execute("DROP TABLE " + deletedTable)
                conn.commit()
            except:
                print("Table Doesn\'t Exist or Mispelled")
        elif cmd == 'add':
            c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            print(c.fetchall())
            addedTable = input("Enter table name to add: ")
            value = input("Enter item value: ")
            try:
                c.execute('CREATE TABLE if not EXISTS ' + addedTable + '(date text, time text, volume int, bid int, ask int, open int, high int, low int, close int, value int)')
                c.execute("INSERT INTO " + addedTable + '(value) VALUES(' + value + ')')
                conn.commit()
                c.execute("SELECT value FROM " + addedTable + ' ORDER BY value DESC LIMIT 1;')
            except:
                print("Table Already Exists or Mispelled")
main()
