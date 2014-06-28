Using the Django StaticFiles App,
STATIC_ROOT points to this folder so that content here is deployable at STATIC_URL
'cstatic' stands for 'collected static' ie using
python manage.py collectstatic -l
This location at cstatic is used a
