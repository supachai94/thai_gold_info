import tkinter as tk
from tkinter import ttk
import urllib.request
import json

root = tk.Tk()
root.title("Thai Gold Info")
root.geometry("500x150")
root.minsize(500, 150)
root.maxsize(500, 150)

# create style
style = ttk.Style()
style.configure("Treeview", font=("Helvetica", 12))

# create treeview
tree = ttk.Treeview(root, columns=("name", "bid", "ask"), style="Treeview")
tree.heading("#0", text="No.", anchor=tk.CENTER)
tree.heading("name", text="Name", anchor=tk.CENTER)
tree.heading("bid", text="Bid", anchor=tk.CENTER)
tree.heading("ask", text="Ask", anchor=tk.CENTER)

# set column width
tree.column("#0", width=50)
tree.column("name", width=200)
tree.column("bid", width=100)
tree.column("ask", width=100)

# add data to treeview
def update_price(countdown=5):
    url = "http://www.thaigold.info/RealTimeDataV2/gtdata_.txt"
    response = urllib.request.urlopen(url)
    data_json = json.loads(response.read())

    # clear previous data
    for i in tree.get_children():
        tree.delete(i)

    # add new data
    count = 1
    for item in data_json:
        if item['name'] == 'GoldSpot' or item['name'] == 'THB' or item['name'] == 'สมาคมฯ':
            name = item['name']
            if name == 'THB':
                name = 'USD - THB'
            if name == 'GoldSpot':
                bid = item['bid']
                ask = item['ask']
                if isinstance(bid, float):
                    bid_str = "{:.2f}".format(bid)
                else:
                    bid_str = bid
                if isinstance(ask, float):
                    ask_str = "{:.2f}".format(ask)
                else:
                    ask_str = ask
            else:
                bid_str = item['bid']
                ask_str = item['ask']
            tree.insert("", "end", text=count, values=(name, bid_str, ask_str))
            count += 1

    root.title(f"Thai Gold Info (Updating in {countdown}s)")
    if countdown == 0:
        countdown = 5
    root.after(1000, update_price, countdown-1)

# set row height
style.configure("Treeview", rowheight=30)

# pack treeview
tree.pack(fill="both", expand=True, padx=10, pady=10)

# start updating data
update_price()

root.mainloop()
