# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()  # declarative system is that one defines a class to be mapped, and then \
#applies to this class a series of directives 

from sqlalchemy import Column, Integer, String

# <codecell>

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    def __repr__(self):  ## __repr__ is optional.
        return "<User(%r, %r)>" % (self.name, self.fullname)

# <codecell>

# the User class now has a Table object associated with it.
User.__table__

# <codecell>

# The Mapper object mediates the relationship between User
# and the "user" Table object.
User.__mapper__

# <codecell>

# User has a default constructor, accepting field names
# as arguments.

ed_user = User(name='ed', fullname='Edward Jones')

# <codecell>

print ed_user

# <codecell>


print(ed_user.name, ed_user.fullname)
print(ed_user.id)

# <codecell>


