
# coding: utf-8

# In[1]:

from sqlalchemy import MetaData, Table, Column, String, Integer


# In[2]:

metadata = MetaData()
user_table = Table('user', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('username', String(50)),
                    Column('fullname', String(50))
                   )


# In[3]:

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)
metadata.create_all(engine)


# In[4]:

#Table has a collection of Column objects,
# which we can access via table.c.<columnname>

user_table.c.username


# In[5]:

# Column is part of a class known as "ColumnElement",
# which exhibit custom Python expression behavior.

user_table.c.username == 'ed'


# In[6]:

# They become SQL when evaluated as a string.
str(user_table.c.username == 'ed')


# In[7]:

# Expressions produce different strings according to *dialect*
# objects.

expression = user_table.c.username == 'ed'
# MySQL....
from sqlalchemy.dialects import mysql
print(expression.compile(dialect=mysql.dialect()))


# In[8]:

# PostgreSQL...
from sqlalchemy.dialects import postgresql
print(expression.compile(dialect=postgresql.dialect()))


# In[10]:

#Reflection
# 'reflection' refers to loading Table objects based on
# reading from an existing database.
metadata2 = MetaData()
user_reflected = Table('user', metadata2, autoload=True, autoload_with=engine)


# In[11]:

print(user_reflected.c) #We can use inspector object to get more database specific details like constraints, types


# In[ ]:



