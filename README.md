![scalable-vector-graphics-book-icon-book-logo-material-200x200-png-clipart-download](https://user-images.githubusercontent.com/102595649/222734460-aad08eaa-c5d2-415e-a5ab-92dbaee20b56.png)

# Library API
- Api service for library managment written in DRF

## Feauters:
- JWT authentication
- Admin panel at /admin/
- Documentation located at /api/doc/swagger/
- Management of borrowings and book returns
- Telegram alerts when a new borrowing is created
- Telegram statistics about overdue borrowings every midnight (Celery)
- Books are automatically hidden and given the status "need_to_refill" when the book inventory reaches 0
- Creating books with two types of covers
- Filtering borrows by status and user ID (customer)

## Endpoints sense:

### USER :

- [POST] /users/register/   (register your user)
- [POST] /users/login/   (login your user)
- [GET] /users/me   (info about yourself)
- [PUT] /users/me   (update all info about yourself)
- [PATCH] /users/me  (partial update of info about yourself)
- [POST] /users/token (get your JWT token for access)
- [POST] /users/token/refresh (update your access token)

### BOOK :

- [POST] /api/library/books/   (create nem book)
- [GET] /api/library/books/   (list of all books)
- [GET] /api/library/books/{id}   (detail info about book)
- [PUT] /api/library/books/{id}   (update all book instance)
- [PATCH] /api/library/books/{id}   (partial update of book instance)
- [DELETE] /api/library/books/{id}   (delete book with chosen id)

### BORROWS :

- [GET] /api/library/borrowings/   (list of all borrowings)
- [GET] /api/library/borrowings/{id}   (detail info about borrow)
- [PUT] /api/library/borrowings/{id}   (update all borrow instance)
- [PATCH] /api/library/borrowings/{id}   (partial update of borrow instance)
- [DELETE] /api/library/borrowings/{id}   (delete borrow with chosen id)
- [DELETE] /api/library/borrowings/{id}/return   (return book with given borrow id)

## Env variables sense:
TELEGRAM_CHAT_ID=<YOUR_TELEGRAM_CHAT_ID>
### Connect telegram alerts on your machine:
1. Add the Telegram BOT to your group.
2. https://api.telegram.org/bot5778173608:AAEkfqphOJjflf0NxOByAvzpPu-RRFkJSpY/getUpdates
3. Look for "chat" object 
- SECRET_KEY=your secret django key (can be random)
- POSTGRES_USER=your database username
- POSTGRES_PASSWORD=your database password
- POSTGRES_DB=your database name
- POSTGRES_HOST=select database image here
- POSTGRES_PORT=5432

## Installing using GitHub:
```python
git clone https://github.com/DevSpaciX/library_api.git
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
open .env.sample and change enviroment variables on yours !Rename file from .env.sample to .env
docker-compose up
```
## Getting access:
- Create user via /api/user/register/
- Get user token via /api/user/token/
- Authorize with it on /api/doc/swagger/ OR 
- Install ModHeader extention and create Request header with value ```Bearer <Your access tokekn>```
## Screenshots:
![2023-03-03_15-37](https://user-images.githubusercontent.com/102595649/222734414-b504c4f3-c5e0-42d7-9624-ebb4d298d76f.png)
![image](https://user-images.githubusercontent.com/102595649/222735049-2cbcb9ce-ced1-42a5-8618-b0a92813fcb4.png)
![image](https://user-images.githubusercontent.com/102595649/222735137-ccd60faa-89a0-407c-832f-db957783cc57.png)
