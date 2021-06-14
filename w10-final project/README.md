Hi,
    My name is Adam Dzierżko, 36 years old, I live in Gdańsk, Poland, central Europe. I work
in a company dealing in the production of electronic devices designed to work in
hazardous areas at risk of gas or coal dust explosion. Most often for mining. The
devices require appropriate certificates and documentation. This created SQL database is
to replace the previous one written in Java.

    The SQL database consists of 5 relatively connected tables. The most important table
is user where the company's employees data are located. Employee id (user_id) is placed
in the remaining 4 tables to see who add or change to any table. An automatically created
datatime in Python is added to each change in the table

    Table of products (produkty) contains manufactured devices. This table
contains columns produkt_id (as primary key), numer (serial number), nazwa (device name),
id of the user (user_id) who made changes to the changes to the table and automatically
generated datatime to save exact time of the change. This table is connected to the table
of description (opis_pr), in which detailed descriptions of individual devices are stored.
Her foregin key is product_id from the product table. The most important part is large
field for a detailed description.

    The table of parts (czesci) works similar to the products table. Contains columns
id of part (czesc_id), name (nazwa), quantity in stock (ilosc), type of part (typ).
The user_id and date columns shows who and when made changes in the table.
Just like in the table of products, table of parts is connected with table
of detailed description of the individual elements in one-to-one relation.

    The application.py program performs all CRUD operations. Delete operations are
cascading, which means removal of product/part will also delete its detailed description.

    In HTML files I used bootstrap modal pop-up windows. The service is more practical,
faster and modern. During update operations, the current values are entered as defaults,
which means that we don't create row from the beginning again, we only change the data
we are interested in in the appropriate column. To view detailed data of product/part
we press the green button description (opis) and we will see it on the pop-up window.
The red button is used to delete row.

I used materials from the following www:
https://mdbootstrap.com
https://getbootstrap.com
https://www.w3schools.com
https://stackoverflow.com

and, of course: CS50 - materials.

Source code is in github repository:
https://github.com/AdamDzierzko/Magazyn-in-Python---CS50-Final-Project

I work for:
http://comonet.eu/en/main-page/
I invite.