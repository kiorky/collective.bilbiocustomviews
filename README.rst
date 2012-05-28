==============================
Introduction
==============================

.. contents::

Credits
========
Companies
---------
|makinacom|_

  * `Planet Makina Corpus <http://www.makina-corpus.org>`_
  * `Contact us <mailto:python@makina-corpus.org>`_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com

Authors
------------

- kiorky  <kiorky@cryptelium.net>

Contributors
-----------------




Description
=================

- This package adds some additionnal views to CMFBibliographyAT:

    - a datatable view for bibliographic folders
    - a summary view for bibliographic folders with everything one lined
    - a selective export facility on a topic containing biblio documents.

It depends on:

    - CMFBibliographyAT
    - eea.facetednaviguation


To enable selectie export:

    - Make a Topic
    - Enable faceted naviguation on it
    - Make the bibliographic search view as default view



Installation pitfalls
-----------------------
- As CMFBibliography reinitialize index values in catalog, you need to install it first, no automatic installation or it.

- jqueryi default profile switch off its css when rexecuted, You also need to install datatables, jqueryui & facetednaviguation first
 
