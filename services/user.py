from passlib.context import CryptContext

from models.user import User
from sqlalchemy.orm import Session
from dto.user import User as UserDTO

# Password thing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# User service


def create_user(data: UserDTO, db: Session):
    # Create a new User object from the Pydantic data
    new_user = User(
        email=data.email,
        name=data.name,
        surname=data.surname,
        hashed_password=get_password_hash(data.hashed_password),
        is_teacher=data.is_teacher,
        grade=data.grade,
        letter=data.letter,
    )
    try:
        # Add the new_user to the database session
        db.add(new_user)
        # Commit the transaction to persist the new user record in the database
        db.commit()
        # Refresh the new_user object to ensure it contains the database-generated ID
        db.refresh(new_user)
    except Exception as e:
        # Handle exceptions, such as database errors, here
        print(e)
        # Optionally, you can raise an exception or return an error response

    # Return the newly created user object
    return new_user


def get_user(id: int, db: Session):
    return db.query(User).filter(User.id == id).first()


def update_user(data: UserDTO, db: Session, id: int):
    # Query the database to find the user by their ID
    user = db.query(User).filter(User.id == id).first()

    # Check if the user exists
    if user:
        # Update the user's properties with data from the Pydantic model
        user.email = data.email
        user.name = data.name
        user.surname = data.surname
        user.is_teacher = data.is_teacher
        user.grade = data.grade
        user.letter = data.letter

        try:
            # Commit the changes to the database
            db.commit()
            # Refresh the user object to ensure it contains the latest data
            db.refresh(user)
        except Exception as e:
            # Handle exceptions, such as database errors, here
            print(e)
            # Optionally, you can raise an exception or return an error response

    return user


def delete_user(db: Session, id: int):
    user = db.query(User).filter(User.id == id).delete()
    db.commit()
    return user
