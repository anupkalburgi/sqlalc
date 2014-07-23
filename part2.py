
# coding: utf-8

# In[35]:

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)


# In[36]:

from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    def __repr__(self):
        return "<User(%r, %r)>" % (
                self.name, self.fullname
            )

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User", backref="addresses")

    def __repr__(self):
        return "<Address(%r)>" % self.email_address

Base.metadata.create_all(engine)


# In[37]:

# a new User object also gains an empty "addresses" collection now.

jack = User(name='jack', fullname='Jack Bean')
jack.addresses


# In[38]:

# populate this collection with new Address objects.

jack.addresses = [
                Address(email_address='jack@gmail.com'),
                Address(email_address='j25@yahoo.com'),
                Address(email_address='jack@hotmail.com'),
                ]


# In[39]:

# the "backref" sets up Address.user for each User.address.

jack.addresses[1]
jack.addresses[1].user


# In[40]:

from sqlalchemy.orm import Session
session = Session(bind=engine)
session.add(jack)
session.new
session.commit()


# In[41]:

# After expiration, jack.addresses emits a *lazy load* when first
# accessed.
jack.addresses


# In[42]:

# the collection stays in memory until the transaction ends.
jack.addresses


# In[ ]:




# In[43]:

session.add_all([
    User(name='wendy', fullname='Wendy Weathersmith'),
    User(name='mary', fullname='Mary Contrary'),
    User(name='fred', fullname='Fred Flinstone')
])
session.commit()


# In[46]:

# collections and references are updated by manipulating objects,
# not primary / foreign key values.

fred = session.query(User).filter_by(name='fred').one()
fred.addresses.append(jack.addresses[1])

fred.addresses


# In[47]:

# Query can select from multiple tables at once.
# Below is an *implicit join*.

session.query(User, Address).filter(User.id == Address.user_id).all()


# In[48]:

# join() is used to create an explicit JOIN.

session.query(User, Address).join(Address, User.id == Address.user_id).all()


# In[49]:

# The most succinct and accurate way to join() is to use the
# the relationship()-bound attribute to specify ON.

session.query(User, Address).join(User.addresses).all()


# In[50]:

# join() will also figure out very simple joins just using entities.

session.query(User, Address).join(Address).all()


# In[51]:

from sqlalchemy.orm import aliased

a1, a2 = aliased(Address), aliased(Address)
session.query(User).        join(a1).        join(a2).        filter(a1.email_address == 'jack@gmail.com').        filter(a2.email_address == 'jack@hotmail.com').        all()


# In[52]:

#Eager Loading
# the "N plus one" problem refers to the many SELECT statements
# emitted when loading collections against a parent result

for user in session.query(User):
    print(user, user.addresses)


# In[53]:

# *eager loading* solves this problem by loading *all* collections
# at once.

session.rollback() # so we can see the load happen again.


# In[55]:

from sqlalchemy.orm import subqueryload
for user in session.query(User).options(subqueryload(User.addresses)):
    print(user, user.addresses)


# In[ ]:



