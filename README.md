CS 340 - Intro to Databases

Porfolio Project - Inpatient Hospital Database


Database project that requires 4 entities to be connected by relationships, including at least 1 Many to Many relationship. My partner and I decided to create a database to help manage an inpatient hospital census. The database manages the relationships between the hospital's patients, doctors, nurses, and hospital units. A school provided MYSQL database is used, along with a Flask framework.

The website application acts as a tool for hospital staff to manage their individual hospital units in regards to patient census. Each unit is meant to operate independently through their unit's page. From there, any patient, doctor, or nurse on the unit can be seen and their profiles accessed. One of the main purposes of the application is to allow unit staff a way to update doctor/patient and nurse/patient assignment. Any new patient must be assigned to a particular unit, doctor, and nurse when admitted. Each shift change requires each patient to be assigned a new doctor and new nurse for the shift. While some project functions may not be realistically necessary for a given page, some functions were added for project requirements and to improve accesibility of project functions.

Patients, doctors, and nurses can all be added, deleted, and updated. Units can be added and updated, but not deleted. There are 1:M relationships between Patients and Nurses, Patients and Doctors, and Patients and Units. There are M:M relationships between Doctors and Units, as well as Nurses and Units. Both Doctors and Nurses can be added to and removed from a Unit.


Partner Credit: Jackson Miller
