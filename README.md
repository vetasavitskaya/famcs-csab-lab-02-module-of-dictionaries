`Python, PyQt5, MS SQL Server`

Два справочника: Renters и Rent Contracts.
![](https://github.com/vetasavitskaya/famcs-csab-lab-02-reference-books-module/blob/main/Rent%20Agency%20Database%20ER%20Diagram.png)

`Renters`
```
CREATE TABLE renters (
  RENTER_ID BIGINT PRIMARY KEY,
  SURNAME VARCHAR(200) NOT NULL,
  NAME VARCHAR(200) NOT NULL,
  PATRONYMIC VARCHAR(200),
  ADRESS VARCHAR(400) NOT NULL,
  PASSPORT_ID VARCHAR(20) NOT NULL UNIQUE,
  DRIVERS_LICENSE VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE rent_contracts (
  CONTRACT_ID BIGINT PRIMARY KEY,
  RENTER_ID BIGINT NOT NULL,
  CAR_NUMBER VARCHAR(10),
  RENT_STARTING_DATE datetime NOT NULL,
  RENT_ENDING_DATE datetime NOT NULL,
  COST DECIMAL(10, 2) NOT NULL,
  FOREIGN KEY (RENTER_ID) REFERENCES renters(RENTER_ID)
);
```



`Rent Contracts`
