# sqtest

* clone
* install packages from requirements.txt
* migrate ```python manage.py migrate```
* create superuser ```pyton manage.py createsuperuser```
* call ```python managae.py test```

## urls

**Content API**

/content_api/contents/

**Navigation API**

/content_api/navigation/ - only root objects

* root1 [pk=1]
* root2 [pk=2]

/content_api/navigation/<pk>/ -- root objects and tree for selected object

/content_api/navigation/5/

* root1 [pk=1]
    * obj3 [pk=3]
        * obj5 [pk=5]
            * obj6 [pk=6]
    * obg4 [pk=4]
* root2 [pk=2]

/content_api/navigation/6/

* root1 [pk=1]
    * obj3 [pk=3]
        * obj5 [pk=5]
            * obj6 [pk=6]
                * obj7 [pk=7]
    * obg4 [pk=4]
* root2 [pk=2]