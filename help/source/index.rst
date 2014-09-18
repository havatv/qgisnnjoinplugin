.. NNJoin documentation master file, created by
   sphinx-quickstart on Sun Feb 12 17:11:03 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NNJoin's documentation!
============================================

Contents:

.. toctree::
   :maxdepth: 2

The QGIS NNJoin Plugin
============================================

The QGIS NNPlugin can be used to join two vector layers (the
*input* and the *join* layer).

A feature from the *input* layer is joined to the nearest
feature in the *join* layer.

The result of the join is a new vector layer with the same
geometry type and coordinate reference system as the *input*
layer.

The result layer will contain all the attributes of both
the *input* and *join* layers plus a new attribute
"distance" that contains the distance between the joined features.
The attributes from the *join* layer will get a prefix
("join_").

The implementation is naive, in that it loops through all
the features of the *input* dataset, and for each feature finds
the nearest neighbour in the *join* dataset.
For point input layers, a spatial index is used to speed up the
search for neighbours.
For line and polygon layers, the geometry of each feature in the
input layer is compared to the geometries of all the features of the
join layer!

Below is a table that cross tabulates *input layer* (rows)
and *join* layer (column) geometry types, and indicates the
usefulness of the plugin (**OK** or
**slow**).

+----------------------------------+-------+-------+---------+
| Layer (row: input; column: join) | Point | Line  | Polygon |
+==================================+=======+=======+=========+
| **Point**                        | OK    | OK    | OK      |
+----------------------------------+-------+-------+---------+
| **Line**                         | Slow! | Slow! | Slow!   |
+----------------------------------+-------+-------+---------+
| **Polygon**                      | Slow! | Slow! | Slow!   |
+----------------------------------+-------+-------+---------+

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

