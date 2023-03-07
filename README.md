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


## Installing using GitHub:
```python
git clone https://github.com/DevSpaciX/library_api.git
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
open .env.sample and change enviroment variables on yours !Rename file from .env.sample to .env
python manage.py migrate
docker run -d -p 6379:6379 redis 
celery -A library_core worker --loglevel=info
celery -A library_core beat --loglevel=info
python manage.py runserver
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
