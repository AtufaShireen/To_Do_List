from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Tasks(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    task = Column(String, default='default-string')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class Todos:
    def __init__(self):
        self.engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        # here
        self.session = Session()
        self.cur_date = datetime.today()

    def add_task(self):
        task_in = input('Enter task\n')
        date_in = input('Enter deadline\n')
        date_in = datetime.strptime(date_in, '%Y-%m-%d')
        new_row = Tasks(task=task_in, deadline=date_in)
        self.session.add(new_row)
        self.session.commit()
        print('The task has been added!\n')

    def tod_task(self):
        rows = self.session.query(Tasks).filter(Tasks.deadline == self.cur_date.date()).all()
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            print(f"Today {datetime.strftime(self.cur_date, '%#d %b')}:")
            for i in range(len(rows)):
                print(f"{i + 1}) {rows[i]}")

    def all_task(self):
        rows = self.session.query(Tasks).order_by(Tasks.deadline).all()
        print("All tasks:")
        for i in range(len(rows)):
            print(f"{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}")

    def week_task(self):
        dates = self.cur_date.date()
        for i in range(7):
            rows = self.session.query(Tasks).filter(Tasks.deadline == dates).all()
            print(f"{dates.strftime('%A %#d %b')}:")
            dates += timedelta(days=1)
            if len(rows) == 0:
                print("Nothing to do!")
                print()
                continue
            for j in range(len(rows)):
                print(f'{j + 1}. {rows[j]}')
            print()

    def miss_task(self):
        rows = self.session.query(Tasks).filter(Tasks.deadline < self.cur_date.date()).order_by(Tasks.deadline).all()
        print('Missed tasks:')
        for i in range(len(rows)):
            print(f"{i + 1}. {rows[i]} {rows[i].deadline.strftime('%#d %b')}")

    def del_task(self):
        print('Choose the number of the task you want to delete:')
        rows=self.session.query(Tasks).order_by(Tasks.deadline).all()
        for i in range(len(rows)):
            print(f"{i+1}) {rows[i].task} {rows[i].deadline.strftime('%#d %b')}")
        det=int(input())
        row=rows[det-1]
        self.session.delete(row)
        self.session.commit()
        print('The task has been deleted!')

    def menu(self):
        while True:
            try:
                task_dis = int(input('\n1) Today\'s tasks\n2) Week\'s tasks\n'
                                     '3) All tasks\n4) Missed tasks\n'
                                     '5) Add task\n6) Delete task\n0) Exit\n'))
            except:
                exit()
            print()
            if task_dis == 1:
                self.tod_task()
                continue
            elif task_dis == 2:
                self.week_task()
            elif task_dis == 5:
                self.add_task()
                continue
            elif task_dis == 3:
                self.all_task()
            elif task_dis == 6:
                self.del_task()
            elif task_dis == 4:
                self.miss_task()
            elif task_dis == 0:
                print('Bye!')
                exit(0)


Todos().menu()
