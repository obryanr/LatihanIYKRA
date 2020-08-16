#!/usr/bin/env python
# coding: utf-8

# In[9]:


import psycopg2
import pandas as pd


# In[10]:


con = psycopg2.connect(user = "postgres",
                              password ='openthedoor1234s',
                              host = "127.0.0.1",
                              port = "5432",
                              database = "dvdrent")

cur = con.cursor()


# ## NO 1

# In[11]:


cur.execute('''
            SELECT COUNT(film_id) 
            FROM film 
            WHERE description LIKE '%stronaut%';
            ''')
myresult = cur.fetchall()

for x in myresult:
  print(f"There are {x[0]} films about astronaut.")


# ## NO 2

# In[35]:


cur.execute('''
            SELECT COUNT(rating) FROM film
            WHERE rating = 'R' AND (replacement_cost BETWEEN 5 AND 15);
            ''')
myresult = cur.fetchall()

for x in myresult:
  print(f"There are {x[0]} films that have a rating of 'R' and replacement cost between $5 and $15.")


# ## NO 3

# In[4]:


cur.execute('''
            SELECT p.staff_id, staffs, COUNT(payment_id) AS Payment_Count, SUM(amount) AS Total_Amount
            FROM (SELECT staff_id, CONCAT(first_name, ' ', last_name) AS staffs FROM staff) AS staff_name
            INNER JOIN payment AS p
            ON p.staff_id = staff_name.staff_id
            GROUP BY p.staff_id, staffs
            ORDER BY total_amount DESC;
            ''')

myresult = cur.fetchall()
df = pd.DataFrame(myresult, columns = ['staff_id', 'staff_name', 'Payment_Count','Total_Amount'])
print('Number of handled payment and total amount by staff members:')
df


# ## NO 4

# In[29]:


cur = con.cursor()
cur.execute('''
            SELECT store_id, rating, ROUND(AVG(replacement_cost), 3) AS avg_rep_cost 
            FROM (SELECT film_id, store_id FROM inventory) AS i
            RIGHT JOIN film AS f
            ON f.film_id = i.film_id
            GROUP BY store_id, rating
            ORDER BY store_id, avg_rep_cost DESC;
            ''')
myresult = cur.fetchall()

#Put myresult into a dataframe
df = pd.DataFrame(myresult, columns = ['store_id', 'rating', 'avg_rep_cost'])

#Transform avg_rep_cost column into numeric
df['avg_rep_cost'] = pd.to_numeric(df['avg_rep_cost'])

#Pivoting
df_pivot = pd.pivot_table(df, values='avg_rep_cost', index='rating', columns='store_id')
df_pivot.sort_values(1.0, ascending=False)


# ## NO 5

# In[30]:


cur.execute('''
            WITH total_payment
            AS
            (
                SELECT customer_id, SUM(amount) AS total_amount
                FROM payment
                GROUP BY customer_id
                ORDER BY total_amount DESC
            )
            SELECT T.customer_id, CONCAT(first_name, ' ', last_name) AS cust_name, email, total_amount
            FROM total_payment AS T
            INNER JOIN customer AS c
            ON T.customer_id = c.customer_id
            LIMIT 5;
            ''')
myresult = cur.fetchall()

#Put myresult into a dataframe
df = pd.DataFrame(myresult, columns = ['customer_id', 'cust_name', 'email', 'total_amount'])
df


# ## NO 6

# In[62]:


cur.execute('''
            SELECT store_id, COUNT(film_id) as NumberofCopies
            FROM inventory
            GROUP BY store_id;
            ''')
myresult = cur.fetchall()

#Put myresult into a dataframe
df = pd.DataFrame(myresult, columns = ['store_id', 'NumberofCopies'])
df


# In[61]:


cur.execute('''
            SELECT title, i.store_id, COUNT(i.film_id) as NumberofCopies
            FROM inventory AS i
            LEFT JOIN film AS f
            ON i.film_id = f.film_id
            GROUP BY title, store_id
            ORDER BY store_id;
            ''')
myresult = cur.fetchall()

#Put myresult into a dataframe
df = pd.DataFrame(myresult, columns = ['title', 'store_id', 'NumberofCopies'])

#Pivoting df
df_pivot2 = pd.pivot_table(df, values='NumberofCopies', index='title', columns='store_id')

#Show sorted pivot table & fill NaN with 0
df_pivot2.fillna(0).astype(int).sort_index()


# ## No 7

# In[65]:


cur.execute('''
            SELECT c.customer_id as id, CONCAT(first_name, ' ', last_name) AS cust_name, email, 
            COUNT(p.customer_id) AS total_transaction
            FROM customer as c
            LEFT JOIN payment as p
            ON c.customer_id = p.customer_id
            GROUP BY id, cust_name, email
            HAVING COUNT(p.customer_id) >= 40
            ORDER BY total_transaction DESC;
            ''')
myresult = cur.fetchall()

#Put myresult into a dataframe
df = pd.DataFrame(myresult, columns = ['cust_id', 'cust_name', 'email', 'total_transaction'])
df


# # PYTHON

# In[1]:


def user_input1():
    input_name = str(input('Input Name: '))
    input_address = str(input('Input Address: '))
    input_dob = str(input('Input D.O.B : '))
    
    print(f"My name is {input_name}, i live in {input_address}, I was born in {input_dob}")
    


# In[2]:


user_input1()


# In[5]:


import re

def user_input2():
    '''
    > user input that contains:
      1. Input_name: User name
      2. Input_address: user address
      3. Input_dob: user day of birth
    
    > character limitator: Regex to limit input_name & input address character
    > dob_limitator: Regex to limit input_dob
    
    Raises:
    ValueError
    1. if there's a non-character in Input_name
    2. if there's a non-character in Input_adress
    3. In Input dob if user doesn't input birthday format correctly (MMMM D, YYYY or MMMM D, YY)
    
    Returns:
    printed out Input_name, input_address, and input_dob in one sentence
    '''
    
    # Limiting user input using RegEx
    character_limitator = re.compile("[a-zA-Z]+$") #Only contain character
    dob_limitator = re.compile("[a-zA-Z]+\s\d{0,2}\,\s(\d{2}|\d{4})+") #Birthday format MMMM D, YYYY or MMMM D, YY

    # User input
    while True:
        try:
            #Input Name
            input_name = str(input('Input name: '))
            if not re.findall(character_limitator, input_name):
                raise ValueError
                
            else:
                while True:
                    try:
                        #Input Address
                        input_address = str(input('Input address: '))
                        if not re.findall(character_limitator, input_address): 
                            raise ValueError #If user doesn't input address correctly it will raise error
                        
                        else:
                            while True:
                                try:
                                    input_dob = str(input('Input D.O.B: '))
                                    if not re.findall(dob_limitator, input_dob): 
                                        raise ValueError #If user doesn't input dob correctly it will raise error
                        
                                    else:
                                        print(f'\nMy name is {input_name},',
                                        f'I live in {input_address},',
                                        f'i was born on {input_dob}')
                                        break
                        
                                except ValueError:
                                    print("\n---Please, use d.o.b format correctly!---\n                                    ---Example: August 17, 1996---")    
                        break
                                          
                    except ValueError:
                        print("\n---Character only!---")
            break
    
        except ValueError:
            print("\n---Character only!---")
        
        


# In[6]:


user_input2()


#  
