<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS><TS version="2.0">
<context>
    <name>NNJoin</name>
    <message>
        <location filename="NNJoin_plugin.py" line="68"/>
        <source>&amp;NNJoin</source>
        <translation>&amp;NN-kopling</translation>
    </message>
    <message>
        <location filename="NNJoin_plugin.py" line="67"/>
        <source>NNJoin</source>
        <translation>NN-kopling</translation>
    </message>
</context>
<context>
    <name>NNJoinDialog</name>
    <message>
        <location filename="NNJoin_gui.py" line="91"/>
        <source>NNJoin</source>
        <translation>NN-kopling</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="99"/>
        <source>No input layer defined</source>
        <translation>Innlaget mangler</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="105"/>
        <source>No join layer defined</source>
        <translation>Koplingslaget mangler</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="115"/>
        <source>Joining</source>
        <translation>Kopler</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="46"/>
        <source>Cancel</source>
        <translation>Avbryt</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="159"/>
        <source>NNJoin finished</source>
        <translation>NN-kopling avsluttet</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="301"/>
        <source>Killing worker</source>
        <translation>Dreper arbeidsprosessen</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="307"/>
        <source>Error</source>
        <translation>Feil</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="315"/>
        <source>Warning</source>
        <translation>Advarsel</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="323"/>
        <source>Info</source>
        <translation>Informasjon</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="48"/>
        <source>OK</source>
        <translation>Kjør</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="47"/>
        <source>Close</source>
        <translation>Avslutt</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="183"/>
        <source>Worker</source>
        <translation>Arbeidsprosessen</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="167"/>
        <source>Aborted</source>
        <translation>Avbrutt</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="169"/>
        <source>No layer created</source>
        <translation>Ikke noe lag</translation>
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
        <location filename="ui_frmNNJoin.ui" line="41"/>
        <source>Input vector layer</source>
        <translation>Innlag</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="91"/>
        <source>Join vector layer</source>
        <translation>Koplingslag</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="175"/>
        <source>Output layer</source>
        <translation>Resultatlag</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="218"/>
        <source>Indicates the progress of the join operation</source>
        <translation>Indikerer framdrifta i arbeidet</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="234"/>
        <source>OK to run the join&lt;br&gt;Close to quit&lt;br&gt;Cancel to abort the join</source>
        <translation>Kjør: Utfør koplinga&lt;br&gt;Avslutt: Avslutt programmet&lt;br&gt;Avbryt: Avbryt programmet</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="55"/>
        <source>The base layer for the join.&lt;br&gt;Each feature of this layer will be joined to the nearest neighbour from the join layer.</source>
        <translation>Basislaget for koplinga.&lt;br&gt;Hvert objekt i dette laget vil bli kopla til det nærmeste objektet i koplingslaget</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="105"/>
        <source>The join layer.&lt;br&gt;A feature from this layer is joined to all the features from the the input layer that has this features as it&apos;s nearest neighbour.</source>
        <translation>Koplingslaget.&lt;br&gt;Et objekt fra dette laget koples til alle de objektene i innlaget som det er nærmeste nabo til</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="181"/>
        <source>The result layer that contains the join.&lt;br&gt;For each feature of the input layer, the output layer contains that feature with all it&apos;s attributes and all the attributes of the nearest feature in the join layer added.</source>
        <translation>Resultatlaget som inneholder koplinga.&lt;br&gt;For hvert objekt i innlaget vil utlaget inneholde objektet med dets attributter pluss attributtene til det nærmestliggende objektet i koplingslaget</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="78"/>
        <source>Use approximate input geometries.&lt;br&gt;This will enable the use of a spatial index - could speed up the join considerably.</source>
        <translation>Benytt forenklede geometrier for innlaget.&lt;br&gt;Dette muliggjør bruk av en romlig indeks, noe som vanligvis får koplinga til å gå fortere.</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="153"/>
        <source>Join prefix:</source>
        <translation>Prefiks:</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="160"/>
        <source>The prefix used for the join layer attributes in the result layer.&lt;br&gt;Without a prefix, if a join layer attribute has the same name as an input layer attribute, it will not be included in the result layer.</source>
        <translation>Prefikset som benyttes for attributter fra koplingslaget i resultatlaget.&lt;br&gt;Uten prefiks vil en miste alle attributter fra koplingslaget som har samme navn som en attributt i inputlaget.</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="163"/>
        <source>join_</source>
        <translation>join_</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="112"/>
        <source>Geometry type:</source>
        <translation>Geometritype:</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="119"/>
        <source>Unknown</source>
        <translation>Ukjent</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="130"/>
        <source>Uses an approximation of the geometry (bounding box) for the join</source>
        <translation>Benytter en tilnærming til geometrien (omsluttende rektangel) for koplinga.</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="81"/>
        <source>Approximate geometries by centroids</source>
        <translation>Tilnærming (sentroider)</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="133"/>
        <source>Approximate by index geometries</source>
        <translation>Tilnærming</translation>
    </message>
</context>
<context>
    <name>Worker</name>
    <message>
        <location filename="NNJoin_engine.py" line="179"/>
        <source>CRS Transformation error!</source>
        <translation>Koordinattransformasjonsfeil!</translation>
    </message>
</context>
</TS>
