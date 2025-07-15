Warehouse & Event Management System
A full-stack solution for managing warehouses, poles, wings, events, arenas, wishlists and archiving —
built with Django + PostgreSQL (backend) and Vue 3 (frontend).

Deployed on AWS: 

Backend & Database: EC2 instance with Docker containers (Django + PostgreSQL)
Frontend: Hosted on an S3 bucket as a static website.


Features
Warehouse Management: Manage poles and wings stored in different warehouses.
Event Management: Create events with start/end dates and assign arenas.
Arena Management: Link arenas to events and allocate poles/wings to arenas.
Wishlist: Select poles and wings for specific arenas via a wishlist interface.
Archiving: Archive completed events, returning stock to warehouses and storing historical records.
Admin Interface: Manage users and models via Django Admin.
REST API: CRUD endpoints for all models with filtering support.
Frontend SPA: Vue 3 app with router for navigating event lists, arena editors, wishlists, and archived events.

Technology Stack
Part	Tech
Backend	Django 5, Django REST Framework, PostgreSQL
Frontend	Vue 3, Vue Router, Axios
Dev tools	Docker, docker-compose
Extras	django-filters, django-cors-headers

The application backend and db run on a AWS EC2. The frontend run on a S3 bucket.

API Overview
Main endpoints
/api/events/ - Create, list, update, delete events
/api/arenas/ - Manage arenas
/api/poles/, /api/wings/ - Manage warehouse items
/api/pole-locations/, /api/wing-locations/ - Manage assignments to arenas
/api/events/:id/full_details/ - Get event with all arenas and their contents
/api/events/:id/archive/ - Archive event, return stock
/api/archived-events/ - View archived events
/api/archived-events/:id/ - Get archived event details

Example Data Flow
Create warehouses, poles, and wings.
Create an event and add arenas to it.
Assign poles and wings to arenas.
After the event, archive it to restore stock and keep historical records.
