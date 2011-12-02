=======================
collective.gmaplocation
=======================

Plone Add-On for managing locations in Google Maps.

This product uses Google Maps API V3.


Features
========

- Location content type

- Search and pick locations on map

- Route planner integration


Installation
============

- Depend your buildout on ``collective.gmaplocation``.

- Install it as Add-On in Plone via control panel or portal setup.


Contributors
============

- Robert Niederreiter

- Jens W. Klein

History
=======

0.2
---

- use content-core macro for location_view.
  [jensens, 2011-12-03]

- feature: unit of map height and width is now available in properties and 
  edit form.
  [jensens, 2011-12-03]

- include a contained buildout, added z3c.autoinclude entry point to setup.py
  [jensens, 2011-12-03]

- LANG.ds is now loaded relative to portal_url
  [jensens, 2011-12-02]

0.1
---

- initial work
  [rnix]
