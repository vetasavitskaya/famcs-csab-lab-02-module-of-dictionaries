`Python, PyQt5, MS SQL

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
```
```
INSERT renters VALUES (1, 'Иванов', 'Иван', 'Иванович', 'Ивановская ул. 1-1, г. Минск', '7637905A001PB1', '000001');
INSERT renters VALUES (2, 'Петров', 'Пётр', 'Петрович', 'Петровская ул. 1-2, г. Минск', '7637905A002PB1', '000002');
INSERT renters VALUES (3, 'Александров', 'Александр', 'Александрович', 'Александровская ул. 1-3, г. Минск', '7637905A003PB1', '000003');
INSERT renters VALUES (4, 'Васильев', 'Василий', 'Васильевич', 'Васильевская ул. 1-4, г. Минск', '7637905A004PB1', '000004');
```


`Rent Contracts`
```
CREATE TABLE rent_contracts (
  CONTRACT_ID BIGINT PRIMARY KEY,
  RENTER_ID BIGINT NOT NULL,
  CAR_NUMBER VARCHAR(10),
  RENT_STARTING_DATE DATE NOT NULL,
  RENT_ENDING_DATE DATE NOT NULL,
  COST DECIMAL(10, 2) NOT NULL,
  FOREIGN KEY (RENTER_ID) REFERENCES renters(RENTER_ID)
);
```
```
INSERT rent_contracts VALUES (1, 1, '1111 AB-1', '2021/10/01', '2021/10/10', 94.5);
INSERT rent_contracts VALUES (2, 2, '2222 AB-2', '2021/10/02', '2021/10/09', 70);
INSERT rent_contracts VALUES (3, 3, '3333 AB-3', '2021/10/03', '2021/10/08', 52.5);
INSERT rent_contracts VALUES (4, 4, '4444 AB-4', '2021-10-04', '2021/10/07', 30.0);
```
