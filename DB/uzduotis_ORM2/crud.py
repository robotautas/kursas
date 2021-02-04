from sqlalchemy.orm import sessionmaker
from model import Order, Customer, Product, Status, OrderProduct, engine

Session = sessionmaker(bind=engine)
session = Session()

def options_list(class_):
    options = session.query(class_).all()
    for i in options:
        print(i, end=' ')


def create_customer():
    f_name = input("First Name: ")
    l_name = input("Last Name: ")
    email = input("Email: ")
    customer = Customer(f_name=f_name, l_name=l_name, email=email)
    session.add(customer)
    session.commit()
    print('created!\n')
    
def create_status():
    print('Existing statuses:')
    options_list(Status)
    name = input("\nEnter new status: ")
    status = Status(name=name)
    session.add(status)
    session.commit()
    print('created!\n')
    
   
def create_product():
    print('Existing products:')
    options_list(Product)
    name = input("\nName: ")
    price = input("Price: ")
    product = Product(name=name, price=price)
    session.add(product)
    session.commit()
    print('created!\n')
    
  
def create_order():
    options_list(Customer)
    customer_id = input("\nCustomer Id: ")
    order = Order(customer_id=customer_id, status_id=1)
    session.add(order)
    session.commit()
    last_order_id = session.query(Order).all()[-1].id
    print('Products available:')
    options_list(Product)
    while True:      
        product_id = input('\nProduct Id: ')
        quantity = input('Quantity: ')
        if product_id and quantity:
            order_product = OrderProduct(order_id=last_order_id, product_id=product_id, quantity=quantity)
            session.add(order_product)
            session.commit()
        else:
            print('created!\n')
            break
    

def get_order():
    last_order_id = session.query(Order).all()[-1].id
    id_ = input(f'Order id (1-{last_order_id}): ') 
    order = session.query(Order).get(id_)
    order_lines = session.query(OrderProduct).filter_by(order_id=order.id)
    print(f'\nOrder #{id_}, customer - {order.customer.f_name} {order.customer.l_name}:')
    print('\nProduct\tQty\tPrice\tSum')
    total = 0
    for line in order_lines:
        print(f'{line.product.name}\t{line.quantity}\t{line.product.price}\t{line.quantity * line.product.price}')
        total += line.product.price * line.quantity
    print(f'\n\t\tTotal:\t{total}')
    print(f'\t\tStatus:\t{order.status.name}')

def change_status():
    last_order_id = session.query(Order).all()[-1].id
    id_ = input(f'Order id (1-{last_order_id}): ') 
    order = session.query(Order).get(id_)
    options_list(Status)
    status_id = input('\nSet status id:')
    order.status_id = status_id
    session.commit()


while True:
    choice = input('c Add Customer | p Add Product | s Add Status | o Add Order | g Get Order | cs Change Status | q Quit\nChoose action: ')
    if choice == 'c':
        create_customer()
    elif choice == 'p':
        create_product()
    elif choice == 's':
        create_status()
    elif choice == 'o':
        create_order()
    elif choice == 'g':
        get_order()
    elif choice == 'cs':
        change_status()
    elif choice == 'q':
        break
    else:
        print('Wrong input!')

session.close()