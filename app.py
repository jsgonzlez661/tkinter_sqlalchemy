import tkinter as tk
from tkinter import ttk
from sqlalchemy import create_engine, select, delete, update
from sqlalchemy.orm import sessionmaker
from models import *

class GUI():

	def __init__(self, root):

		# Database Conection
		engine = create_engine('mysql+mysqlconnector://root:@127.0.0.1:3306/task')
		Session = sessionmaker(bind=engine)
		session = Session()
		Base.metadata.create_all(engine)

		self.root=root
		self.root.title("TASK APP")
		self.root.resizable(0,0)
		# self.root.geometry("400x400")
		self.root.config(bg="#CFE0F4")		

		self.frame = tk.Frame(self.root, bg="#F6F4F5")
		self.frame.grid(row=0, column=0, padx=5, pady=5)

		self.label = tk.Label(self.frame, text="TASK APP", font=("Lobster 1.4", 30), bg="#F6F4F5")
		self.label.grid(row=0, column=0, columnspan=4, sticky="WNES", padx=5, pady=5)

		self.entry = tk.Entry(self.frame, font=("Lobster 1.4", 15), width=30,relief="flat", borderwidth=12)
		self.entry.grid(row=1, column=0, columnspan=4, sticky="WNES", padx=5, pady=5)

		self.bt = tk.Button(self.frame, text="SAVE", height=2, relief="flat", bg="#191919", foreground="white", activebackground="#d9534f", overrelief=tk.FLAT, bd=0, activeforeground="white", font=("HelveticaNeue",10), command=lambda:insert_task(self.entry, self.treeview))
		self.bt.grid(row=2, column=0, columnspan=4, sticky="WNES", padx=10, pady=10)

		def get_task():
			elementos  = self.treeview.get_children()
			for elemt in elementos:
				self.treeview.delete(elemt)

			stmt = select('*').select_from(Task)
			result = session.execute(stmt).fetchall()
			for row in result:
				stateNum = row[2]
				if(stateNum==1):
					stateNum = "Done"
				else:
					stateNum =	"Incomplete"		
				self.treeview.insert("", "end", text=row[1], values=(stateNum))

		def delete_task(treeview):
			remove = treeview.selection()[0]
			value = self.treeview.item(remove)['text']
			if(remove!=()):
				u = delete(Task).where(Task.name==value)
				result = session.execute(u)
				session.commit()
				get_task()		

		def insert_task(entry, treeview):
			task_name = entry.get()
			if(task_name!=""):
				task = Task(name=task_name, state=False)
				session.add(task)
				session.commit()
				get_task()

		def state_task(treeview):
			state = treeview.selection()[0]
			value = self.treeview.item(state)['values'][0]
			name = self.treeview.item(state)['text']
			if(state!=()):
				u = update(Task).where(Task.name==name)
				if(value=='Incomplete'):
					u = u.values(state=1)
					self.treeview.item(state, values=("Done"))
				else:
					u = u.values(state=0)
					self.treeview.item(state, values=("Incomplete"))
				result = session.execute(u)
				session.commit()
				get_task()

		s = ttk.Style()
		self.treeview = ttk.Treeview(self.frame, show="tree", columns=("state"))
		s.configure('Treeview', font = ('HelveticaNeue', 12))
		self.treeview.grid(row=3, column=0, columnspan=4, sticky="NEWS", padx=5, pady=5)
		self.scroll_treeview =tk.Scrollbar(self.frame, command=self.treeview.yview)             
		self.scroll_treeview.grid(row=3, column=3, sticky="NES")

		self.treeview.config(yscrollcommand=self.scroll_treeview.set)
		self.treeview.column("#0", anchor="w", width=300) 
		get_task()
		
		self.bt_done = tk.Button(self.frame, text="DONE", relief="flat", bg="#5cb85c", foreground="white", activebackground="#d9534f", overrelief=tk.FLAT, bd=0, activeforeground="white", font=("HelveticaNeue",10), command=lambda:state_task(self.treeview))
		self.bt_done.grid(row=4, column=0, columnspan=2, sticky="NEWS")

		self.bt_delete = tk.Button(self.frame, text="DELETE", relief="flat", bg="#d9534f", foreground="white", activebackground="#292b2c", overrelief=tk.FLAT, bd=0, activeforeground="white", font=("HelveticaNeue",10), command=lambda:delete_task(self.treeview))
		self.bt_delete.grid(row=4, column=2, columnspan=2, sticky="NEWS")


if __name__ == '__main__':
	root = tk.Tk()
	app = GUI(root)
	root.mainloop()