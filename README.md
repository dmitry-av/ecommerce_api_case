# Stripe API Backend

stripe.com/docs is a payment system with a detailed API and a free test mode for simulating and testing payments. Using the Python library called Stripe, you can easily create various types of payment forms, store customer data, and implement other payment functions.

## Running via Docker

In the "djngo.env" file, specify the public and secret API keys from Stripe https://dashboard.stripe.com/test/apikeys, , as well as set the Django secret key.  
Run the command: docker-compose up --build  
The website will be accessible at http://localhost:4000/  

## API Description

In the Django Admin panel, you can view and edit objects (Item, Order, OrderItem). Three test Items have been added with IDs 1, 2, and 3.

You can pay for individual items or collect items into an order:
Making a GET request to **/item/{id}** will retrieve an HTML page with a BUY button. After that, a request is made to the Stripe Session Form, allowing you to make a payment for the individual item.
Making an empty POST request to **/orders** will return a response with the ID of the created Order. After that, by sending a POST request to **/orders/{order id}/items/** in the following format:

{  
"product_id": {item id},  
"quantity": {quantity}  
}

You can make unlimited requests of this type, adding new items to the order each time.
To pay for the created order:  
Making a GET request to **/order/{order id}** returns HTML with a payment button. Furthermore, a Stripe Session will be generated (the payment form will include all the items added to the order and the total amount).

<div>
<img src="https://github.com/dmitry-av/ecommerce_api_case/assets/101987388/8dbe1bcd-ef68-45ce-b288-a529b875e82d" alt="drawing" width="500"/>  
</div>
<div>
<img src="https://github.com/dmitry-av/ecommerce_api_case/assets/101987388/cb18f4b8-8c3b-41f3-9b2b-6786e45c0a77" alt="drawing" width="500"/>  
</div>


