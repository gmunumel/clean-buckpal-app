from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    """
    Address class representing a user's address.
    """

    street_name: str
    street_number: int
    city: str
    postal_code: str
    country: str

    def __repr__(self) -> str:
        return (
            f"Address(street_name={self.street_name!r}, street_number={self.street_number!r}, "
            f"city={self.city!r}, postal_code={self.postal_code!r}, country={self.country!r})"
        )
