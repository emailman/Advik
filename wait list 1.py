"""
Allow names to be added to a wait list
Pull names from the wait list using FIFO
"""

from guizero import *


def main():
    def add_name():
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

    customers = []
    app = App("Customer Waiting List")
    app.text_size = 14

    Text(app, "Enter Your Name Below")
    tbx_name = TextBox(app, width="20")

    PushButton(app, text="Click to Add Your Name", command=add_name)

    lbx_names = ListBox(app)

    PushButton(app, text="Click to Service Next Customer", command=service_customer)

    app.display()


if __name__ == "__main__":
    main()
