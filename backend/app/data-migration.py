import csv
from datetime import datetime
from app.db.database import SessionLocal, Base, engine
from app.db.models import User, Investor, Commitment
from app.commons import UserType, InvestorType

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def string_to_investor_type(investor_type_str):
    # Normalize the input: convert to lowercase, replace spaces with underscores
    normalized_str = investor_type_str.lower().replace(" ", "_")

    # Attempt to get the corresponding InvestorType value
    try:
        return InvestorType(normalized_str)
    except ValueError:
        raise ValueError(f"'{investor_type_str}' is not a valid InvestorType")


def migrate_data(csv_file: str):
    # Create a session to interact with the database
    db = SessionLocal()

    try:
        # Open and read the CSV file
        with open(csv_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Generate a unique email for the investor (just for reference)
                user_email = (
                    row["Investor Name"].lower().replace(" ", ".") + "@example.com"
                )

                # Check if user already exists
                user = db.query(User).filter(User.email == user_email).first()

                if not user:
                    # If user does not exist, create a new user
                    user = User(
                        name=row["Investor Name"],
                        country=row["Investor Country"],
                        user_type="INVESTOR",  # Assuming a user type, change as needed
                        email=user_email,
                        created_at=datetime.strptime(
                            row["Investor Date Added"], "%Y-%m-%d"
                        ),
                        updated_at=datetime.strptime(
                            row["Investor Last Updated"], "%Y-%m-%d"
                        ),
                    )
                    db.add(user)
                    db.commit()
                    db.refresh(user)  # Refresh user to get the ID

                # Check if investor already exists
                investor = (
                    db.query(Investor).filter(Investor.email == user_email).first()
                )

                if not investor:
                    # If investor does not exist, create a new investor
                    investor = Investor(
                        name=row["Investor Name"],
                        email=user_email,
                        country=row["Investor Country"],
                        user_id=user.id,  # Reference to the user
                        investor_type=string_to_investor_type(row["Investor Type"]),
                        created_at=datetime.strptime(
                            row["Investor Date Added"], "%Y-%m-%d"
                        ),
                        updated_at=datetime.strptime(
                            row["Investor Last Updated"], "%Y-%m-%d"
                        ),
                    )
                    db.add(investor)
                    db.commit()
                    db.refresh(investor)  # Refresh investor to get the ID

                # Insert Commitment Data (always insert commitment)
                commitment = Commitment(
                    asset_class=row["Commitment Asset Class"],
                    amount=float(row["Commitment Amount"]),
                    currency=row["Commitment Currency"],
                    investor_id=investor.id,  # Reference to the investor
                    created_at=datetime.strptime(
                        row["Investor Date Added"], "%Y-%m-%d"
                    ),
                    updated_at=datetime.strptime(
                        row["Investor Last Updated"], "%Y-%m-%d"
                    ),
                )
                db.add(commitment)
                db.commit()

        print("Data migration completed successfully!")

    except Exception as e:
        db.rollback()  # In case of error, rollback the transaction
        print(f"Error during migration: {e}")
    finally:
        db.close()


# Run the migration script on your CSV file
if __name__ == "__main__":
    # Specify the correct CSV file path here
    csv_file = "./data.csv"
    migrate_data(csv_file)
