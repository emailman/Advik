"""
Allow names to be added to a wait list
Pull names from the wait list using FIFO
"""

from guizero import *


def main():
    def add_name():
        if tbx_name.value:
            customers.append(tbx_name.value)
            tbx_name.clear()
            show_names()

    def show_names():
        lbx_names.clear()
        for customer in customers:
            lbx_names.append(customer)

    def service_customer():
        if customers:
            customer = customers.pop(0)
            info(title='Customer Service', text=f"Now serving {customer}")
            show_names()
        else:
            info(title="Customer Service", text="No customers to serve")

    def key_pressed(clicked):
        if  clicked.key == "\r":
            add_name()

    customers = []
    app = App("Customer Waiting List")
    app.text_size = 14

    Text(app, "Enter Your Name Below, then <enter>", size="12")
    tbx_name = TextBox(app, width="20")
    tbx_name.when_key_pressed = key_pressed

    lbx_names = ListBox(app)

    PushButton(app, text="Click to Service Next Customer",
               command=service_customer)

    app.display()


if __name__ == "__main__":
    main()
