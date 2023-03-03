# Cinema API
- Api service for cinema managment written on DRF

## Feauters:
- JWT authenticated
- Admin panel /admin/
- Documentation is located via /api/doc/swagger/
- Managing borrowings and return books
- Telegram alerts when new borrow is created
- Telegram statistic about overdue borrowings every midnight ( celery )
- Book automatickly hiding and getting status need_to_refill if book inventory = 0
- Creating books with 2 types of covers 
- Filtering borrows by status and user id ( customer )
- Docker app starts only when db is available ( custom command via management/commands )

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
