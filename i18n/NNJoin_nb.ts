<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS><TS version="2.0">
<context>
    <name>NNJoin</name>
    <message>
        <location filename="NNJoin_plugin.py" line="76"/>
        <source>&amp;NNJoin</source>
        <translation>&amp;NN-kopling</translation>
    </message>
    <message>
        <location filename="NNJoin_plugin.py" line="75"/>
        <source>NNJoin</source>
        <translation>NN-kopling</translation>
    </message>
    <message>
        <location filename="NNJoin_plugin.py" line="231"/>
        <source>Information</source>
        <translation>Informasjon</translation>
    </message>
    <message>
        <location filename="NNJoin_plugin.py" line="231"/>
        <source>Vector layers not found</source>
        <translation>Ingen vektorlag</translation>
    </message>
</context>
<context>
    <name>NNJoinDialog</name>
    <message>
        <location filename="NNJoin_gui.py" line="61"/>
        <source>NNJoin</source>
        <translation>NN-kopling</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="133"/>
        <source>No input layer defined</source>
        <translation>Innlaget mangler</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="139"/>
        <source>No join layer defined</source>
        <translation>Koplingslaget mangler</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="157"/>
        <source>Joining</source>
        <translation>Kopler</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="62"/>
        <source>Cancel</source>
        <translation>Avbryt</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="209"/>
        <source>NNJoin finished</source>
        <translation>NN-kopling avsluttet</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="503"/>
        <source>Killing worker</source>
        <translation>Dreper arbeidsprosessen</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="510"/>
        <source>Error</source>
        <translation>Feil</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="518"/>
        <source>Warning</source>
        <translation>Advarsel</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="526"/>
        <source>Info</source>
        <translation>Informasjon</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="65"/>
        <source>OK</source>
        <translation>Kjør</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="63"/>
        <source>Close</source>
        <translation>Avslutt</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="234"/>
        <source>Worker</source>
        <translation>Arbeidsprosessen</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="219"/>
        <source>Aborted</source>
        <translation>Avbrutt</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="221"/>
        <source>No layer created</source>
        <translation>Ikke noe lag</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="64"/>
        <source>Help</source>
        <translation>Hjelp</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="314"/>
        <source>Information</source>
        <translation></translation>
    </message>
</context>
<context>
    <name>NNJoinDialogBase</name>
    <message>
        <location filename="ui_frmNNJoin.ui" line="14"/>
        <source>NNJoin</source>
        <translation>NN-kopling</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="44"/>
        <source>Input vector layer</source>
        <translation>Innlag</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="122"/>
        <source>Join vector layer</source>
        <translation>Koplingslag</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="237"/>
        <source>Output layer</source>
        <translation>Resultatlag</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="323"/>
        <source>Indicates the progress of the join operation</source>
        <translation>Indikerer framdrifta i arbeidet</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="339"/>
        <source>OK to run the join&lt;br&gt;Close to quit&lt;br&gt;Cancel to abort the join</source>
        <translation>Kjør: Utfør koplinga&lt;br&gt;Avslutt: Avslutt programmet&lt;br&gt;Avbryt: Avbryt programmet</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="64"/>
        <source>The base layer for the join.&lt;br&gt;Each feature of this layer will be joined to the nearest neighbour from the join layer.</source>
        <translation>Basislaget for koplinga.&lt;br&gt;Hvert objekt i dette laget vil bli kopla til det nærmeste objektet i koplingslaget</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="142"/>
        <source>The join layer.&lt;br&gt;A feature from this layer is joined to all the features from the the input layer that has this features as it&apos;s nearest neighbour.</source>
        <translation>Koplingslaget.&lt;br&gt;Et objekt fra dette laget koples til alle de objektene i innlaget som det er nærmeste nabo til</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="249"/>
        <source>The result layer that contains the join.&lt;br&gt;For each feature of the input layer, the output layer contains that feature with all it&apos;s attributes and all the attributes of the nearest feature in the join layer added.</source>
        <translation>Resultatlaget som inneholder koplinga.&lt;br&gt;For hvert objekt i innlaget vil utlaget inneholde objektet med dets attributter pluss attributtene til det nærmestliggende objektet i koplingslaget</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="213"/>
        <source>Join prefix:</source>
        <translation>Prefiks:</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="223"/>
        <source>join_</source>
        <translation>join_</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="149"/>
        <source>Geometry type:</source>
        <translation>Geometritype:</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="161"/>
        <source>Unknown</source>
        <translation>Ukjent</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="97"/>
        <source>Approximate geometries by centroids</source>
        <translation>Tilnærming (sentroider)</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="220"/>
        <source>The prefix used for the join layer attributes in the result layer.&lt;br&gt;Without a prefix, a join layer attribute that has the same name as an input layer attribute will not be included in the result layer.</source>
        <translation>Prefikset som benyttes for attributter fra koplingslaget i resultatlaget.&lt;br&gt;Uten prefiks vil en miste alle attributter fra koplingslaget som har samme navn som en attributt i innlaget.</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="175"/>
        <source>Approximate geometries</source>
        <translation>Omtrentlige geometrier</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="182"/>
        <source>Use an index to speed up the join</source>
        <translation>Bruk en romlig indeks for å få koplinga til å gå fortere</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="185"/>
        <source>Use index</source>
        <translation>Bruk indeks</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="94"/>
        <source>Use approximate input geometries.&lt;br&gt;The result will also be approximate.&lt;br&gt;Could speed up the join considerably.</source>
        <translation>Bruk tilnærmede inngeometrier.&lt;br&gt;Resultatet vil også være tilnærma.&lt;br&gt;Kan få koplinga til å gå fortere.</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="172"/>
        <source>Uses an approximation of the geometry (bounding box) for the join.&lt;br/&gt;The result will also be approximate.</source>
        <translation>Bruk tilnærma koplingsgeometri.&lt;br&gt;Resultatet vil også være tilnærma.</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="355"/>
        <source>Get some help</source>
        <translation>Få hjelp</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="358"/>
        <source>Help</source>
        <translation>Hjelp</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="274"/>
        <source>Neighbour distance field:</source>
        <translation>Felt for naboavstand</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="281"/>
        <source>The field name used for the distance to the nearest neighbour.&lt;br&gt;Can not be the same as an existing field name.</source>
        <translation>Navnet på feltet med avstand til nærmeste nabo.&lt;br&gt;Kan ikke være likt et eksisterende feltnavn</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="284"/>
        <source>distance</source>
        <translation>avstand</translation>
    </message>
</context>
<context>
    <name>Worker</name>
    <message>
        <location filename="NNJoin_engine.py" line="358"/>
        <source>CRS Transformation error!</source>
        <translation>Koordinattransformasjonsfeil!</translation>
    </message>
</context>
</TS>
