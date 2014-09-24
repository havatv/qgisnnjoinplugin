.. NNJoin documentation master file, created by
   sphinx-quickstart on Sun Feb 12 17:11:03 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The QGIS NNJoin Plugin
============================================

Contents:

.. toctree::
   :maxdepth: 2

Functionality
----------------------------

- The QGIS NNPlugin can be used to join two vector layers (the *input*
  and the *join* layer).

- All geometry type combinations are supported.

- A feature from the *input* layer is joined to the nearest
  feature in the *join* layer.

- The result of the join is a new vector layer with the same
  geometry type and coordinate reference system as the *input*
  layer.

- Joining layers with different Coordinate Reference Systems (CRS) is
  supported.
  A warning is given when the user attempts to join layers with
  different CRS.

- Self joins are supported.
  For self joins, each feature in the layer is joined to its nearest
  neighbour within the layer.

The result layer
---------------------------------

The result layer will contain all the attributes of both
the *input* and *join* layers plus a new attribute
"distance" that contains the distance between the joined features.
The attributes from the *join* layer will get a prefix
(the default "join\_", but this can be set by the user).
If a join prefix is not used, attributes from the join layer that
have the same name as attributes in the input layer will not be
included in the output layer.

Options
--------------------------
- The user can choose to use an approximation of the input geometry
  (the centroid - *QgsGeometry.centroid*) to allow the use of spatial
  indexes also for non-point input layers.

- The user can choose to use a spatial index for the join layer if the
  input layer is a point layer.
  The results will not be exact (the join is based on the geometry
  approximation of the spatial index).

- The user can choose the prefix of the join layer attributes in the
  output layer.

- The user can choose the name of the result layer.

Performance
--------------------------

Below is a table that cross tabulates *input layer* (rows)
and *join* layer (column) geometry types, and indicates the
usefulness of the plugin (**OK** or **slow**).

.. table:: Efficiency of NNJoin for simple geometries

    +----------------------------------+-------+-------+---------+
    | Layer (row: input; column: join) | Point | Line  | Polygon |
    +==================================+=======+=======+=========+
    | **Point**                        | OK    | Slow! | Slow!   |
    +----------------------------------+-------+-------+---------+
    | **Line**                         | Slow! | Slow! | Slow!   |
    +----------------------------------+-------+-------+---------+
    | **Polygon**                      | Slow! | Slow! | Slow!   |
    +----------------------------------+-------+-------+---------+

Multi geometries:

.. table:: Efficiency of NNJoin for multigeometries

    +----------------------------------+------------+------------+--------------+
    | Layer (row: input; column: join) | MultiPoint | MultiLine  | MultiPolygon |
    +==================================+============+============+==============+
    | **MultiPoint**                   | Slow!      | Slow!      | Slow!        |
    +----------------------------------+------------+------------+--------------+
    | **MultiLine**                    | Slow!      | Slow!      | Slow!        |
    +----------------------------------+------------+------------+--------------+
    | **MultiPolygon**                 | Slow!      | Slow!      | Slow!        |
    +----------------------------------+------------+------------+--------------+

Implementation
-----------------------------------

Looping through the features of the *input* layer, the nearest
neighbour to each feature is identified in the *join* layer.

A spatial index on the join layer may speed up the join.
*QgsSpatialIndex* provides the *nearestNeighbor* function, and
this function returns the nearest neighbour(s) to a given point
among the index geometries (which are approximations of the
original geometries).

If the geometry type of the input layer is point, a spatial index on
the join layer can be used.
For join layers with geometry type point, the index geometries are
identical to the original geometries, so the join should be exact.

For join layers with geometry type other than point, the join will
not be exact.

For input layers with non-point geometry type, the user can force an
index on the join layer to be allowed by checking
"Approximate geometries using centroids".
In that case the join will not be exact.

For input layers with geometry type Point (or centroid
approximations) and join layers with geometry type point, a spatial
index on the join layer is created, and the
*QgsSpatialIndex.nearestNeighbor* function of this index is used to
find the nearest neighbour for each input feature.

For input layers with geometry type point (or centroid
approximations) and join layers with a non-point geometry type, the
user can choose to use an index on the join layer, but in that case
the approximated geometry of the join layer is used in the join.

For input layers with other geometry types, the default is to use
the *QgsGeometry.distance* function to find the distance between
geometries.
The feature of the join layer that has the shortest distance to the
the geometry of the input feature is chosen as the nearest
neighbour.
This means that the geometry of each feature of the input layer has
to be compared to the geometry of all the features in the join
layer!

.. table:: NNJoin geometry types, join options and index usage

    +----------------------------------+------------------------------+-----------+------------------------------+
    | Layer (row: input; column: join) | Point                        | Non-point | Non-point, index chosen      |
    +==================================+==============================+===========+==============================+
    | **Point**                        | Spatial index used           | No index  | Spatial index used (inexact) |
    +----------------------------------+------------------------------+-----------+------------------------------+
    | **Non-point**                    | No index                     | No index  | NA                           |
    +----------------------------------+------------------------------+-----------+------------------------------+
    | **Non-point, approximate**       | Spatial index used (inexact) | No index  | Spatial index used (inexact) |
    +----------------------------------+------------------------------+-----------+------------------------------+

If the input and join layers have different Coordinate Reference
Systems (CRS), the input geometry is transformed to the join layer
CRS before the join is performed.

Versions
----------------------------------

The current version is 1.1.0

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
