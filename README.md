Warehouse & Event Management System

A full-stack solution for managing:

      -warehouse
      -poles & wings inventory
      -events & arena
      -wishlist
      -archiving completed events

Built with:

    -Django + PostgreSQL (backend)
    -Vue 3 (frontend SPA)

Deployed on AWS:

    -Backend & Database: EC2 instance running Docker containers (Django + PostgreSQL)
    -Frontend: Hosted on an S3 bucket as a static Vue site

Features

    -Warehouse Management: Manage poles & wings stored in different warehouses.
    -Event Management: Create events with start/end dates and assign arenas.
    -Arena Management: Link arenas to events, allocate poles & wings to arenas.
    -Wishlist: Select poles & wings for specific arenas via a wishlist interface.
    -Archiving: Archive completed events, automatically return stock to warehouses, keep historical records.
    -Admin Interface: Manage users and models via Django Admin.
    -REST API: Full CRUD endpoints for all models, with filtering support.
    -Frontend SPA: Vue 3 app with router for navigating events, arenas, wishlists, and archived events.

Technology Stack

    Backend:    	Django 5, Django REST Framework, PostgreSQL
    Frontend:    	Vue 3, Vue Router, Axios
    Dev tools:  	Docker, docker-compose
    Extras:      	django-filters, django-cors-headers


Example Data Flow

    -> Create warehouses, poles, and wings.
    
    -> Create an event and add arenas to it.
    
    -> Assign poles & wings to arenas.
    
    -> After the event is finished, archive it:
     
    -> Stock is automatically restored to warehouses.
    
    -> Full history is saved for records.

