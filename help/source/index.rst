.. NNJoin documentation master file.

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
  supported, as long as the join layer coordinate system is a
  projected CRS.

  A warning is given when the user attempts to join layers with
  different CRS.
  
  The join and distance calculations is performed using the join
  layer CRS.

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

- If the input layer is a point layer and the join layer is not a
  point layer, the user can choose to base the join on the simplified
  geometries of the spatial index for the join layer.
  The results will not be exact, but the speed should increase.

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
    | **Point**                        | OK    | OK    | OK      |
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

For input layers with geometry type point (or centroid
approximation), a spatial index on the join layer will be used.

For join layers with geometry type other than point, the user can
choose to do an inexact join based on the join layer index
geometries to speed up the join by checking
"Approximate by index geometries".

For input layers with non-point geometry type, the user can specify
that the geometry centroids are used for the join by checking
"Approximate geometries by centroids".
This means that the join will not be exact with respect to the
original input layer geometries.

When a spatial index on the join layer is available, the
*QgsSpatialIndex.nearestNeighbor* function of the index is used to
find the nearest neighbour for each input feature.

For input layers with other geometry types than point, the default
is to use the *QgsGeometry.distance* function to find the distance
between geometries.
The feature of the join layer that has the shortest distance to the
the geometry of the input feature is chosen as the nearest
neighbour.
This means that the geometry of each feature of the input layer has
to be compared to the geometry of all the features in the join
layer!

.. table:: NNJoin geometry types, join options and index usage (non-multi geometry types)

    +----------------------------------+------------------------------+--------------------+------------------------------+
    | Layer (row: input; column: join) | Point                        | Non-point          | Non-point, index chosen      |
    +==================================+==============================+====================+==============================+
    | **Point**                        | Spatial index used           | Spatial index used | Spatial index used (inexact) |
    +----------------------------------+------------------------------+--------------------+------------------------------+
    | **Non-point**                    | No index                     | No index           | NA                           |
    +----------------------------------+------------------------------+--------------------+------------------------------+
    | **Non-point, approximate**       | Spatial index used (inexact) | No index           | Spatial index used (inexact) |
    +----------------------------------+------------------------------+--------------------+------------------------------+

If the input and join layers have different Coordinate Reference
Systems (CRS), the input geometry is transformed to the join layer
CRS before the join is performed.

The join will fail if transformation between the input layer CRS and
the join layer CRS is not possible.

**The join layer should have a projected CRS**.

Versions
----------------------------------

The current version is 1.2.0

Misc
------

QGIS Plugin page: NNJoinPlugin_

Code repository: NNJoinRepository_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _NNJoinRepository: https://github.com/havatv/qgisnnjoinplugin.git
.. _NNJoinPlugin: https://plugins.qgis.org/plugins/NNJoin/