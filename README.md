qgisnnjoinplugin
================

A QGIS plugin that performs a nearest neighbour join on two
vector layers.

For each feature of the input layer, the nearest feature of
the join layer is found, and the distance between the two
features is calculated.

The result of the operation is a new vector layer.
A feature in the result layer will have the geometry and
attributes of one of the features in the input layer plus the
attributes of the nearest feature in the join layer.  In
addition, a new attribute is added that contains the distance
between the two neighbouring features.
