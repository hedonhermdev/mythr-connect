# MythrConnect
  MythrConnect is a mini social media website that I'm building for the DVM WinterAssignment task. 
  The project is currently in Phase1 of the task. (I'm moving to Phase2)  
  
 # Project Status
  The following are the essential features I have to implement in phase1: 
  - [x] Implement user authentication. Django has a built in auth system and we expect you to use it (it's part of Django's "batteries included" appeal). It's a really handy session based auth system.
  - [x] Create a well defined database structure and then implement it in the models.
  - [x] Associate users with a profile. Let users modify their profile data.
  - [x] Allow users to make their own posts and also comment on others' posts (no need to implement commenting on comments).
  - [x] Allow users to follow each other (hint: you'll need to use many-to-many fields). When you follow other users, make it so that the relavent posts can easily be accessed somewhere (sort of like a news feed).
  - [ ] Make it possible to edit and delete posts. But think about this issue: what if someone posts something offensive and then edits or deletes it.... how would you prevent cyber-crime and cyber-bullying caused by this? (this is an example of where your creativity as a developer will be needed)

Phase 2 features: 
  - [ ] Up until now, you've only been using an Sqlite3 database. Time to upgrade. Change your database backend to MySQL (since it's part of the DVM's tech stack).
  - [ ] Add a profile pictures feature. For this you'll need to learn how to store and reference/retrieve files and images in     Django. You'll also probably need to learn how to do some image formatting using Pillow.
  - [ ] Without using the student pack that you got, make a seperate account on SendGrid. Then using SendGrid's API, extend the "following other people" feature so that you can choose to recieve mail based notificiations whenever that person makes a new post (so now there are two ways to follow a person.)
  - [ ] Extend the login system. Make it so that a person can also log in with Google. Use Google's API to provide OAUTH 2.0 based log-in.
  - [ ] Create a feature where staff and site admins can generate a report containing all of the basic profile data of each person registered on the site. The profile should be in the form of an excel sheet and we suggest using Openpyxl to get this done in python.
  
