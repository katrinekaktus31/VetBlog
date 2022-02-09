# VetBlog
This site provides the opportunity to conduct online consultations with veterinarians, by correspondence between doctor and patient.

# Ways to set up a work environment.
requirements.txt - the file contains the necessary libraries to create a virtual environment.
The important technologies: Python 3.7, Django, PostgreSQL

# Implementation

The project has one app (vet folder). The structure of the created database is described in model.py.
Users register through special forms forms.py, data validation takes place at the django level.
Admin rights are granted by the superuser to other users through the django admin platform. Only site administrator can edit posts and add new diseases. 
Only site superuser can delete another users.

The statics and media folder have been added specifically to allow the reader to use this data. (git clone, anyway)
Therefore, the site was not deployed so does not have a whitenoise library implementation.

The gmail platform used for correspondence. The logic of receiving letters in services.py
Email for the customer contact website - vetReproductionNUBip@gmail.com

For any questions write to the mail mentioned above.

# Required variables
DATABASES = {'USER','PASSWORD'}
EMAIL = {'EMAIL_HOST_PASSWORD'}


