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
        <location filename="NNJoin_gui.py" line="102"/>
        <source>No input layer defined</source>
        <translation>Innlaget mangler</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="108"/>
        <source>No join layer defined</source>
        <translation>Koplingslaget mangler</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="121"/>
        <source>Joining</source>
        <translation>Kopler</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="46"/>
        <source>Cancel</source>
        <translation>Avbryt</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="165"/>
        <source>NNJoin finished</source>
        <translation>NN-kopling avslutta</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="336"/>
        <source>Killing worker</source>
        <translation>Dreper arbeidsprosessen</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="342"/>
        <source>Error</source>
        <translation>Feil</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="350"/>
        <source>Warning</source>
        <translation>Advarsel</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="358"/>
        <source>Info</source>
        <translation>Informasjon</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="48"/>
        <source>OK</source>
        <translation>Køyr</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="47"/>
        <source>Close</source>
        <translation>Avslutt</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="191"/>
        <source>Worker</source>
        <translation>Arbeidsprosess</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="175"/>
        <source>Aborted</source>
        <translation>Avbrote</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="177"/>
        <source>No layer created</source>
        <translation>Ikkje noko lag</translation>
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
        <location filename="ui_frmNNJoin.ui" line="111"/>
        <source>Join vector layer</source>
        <translation>Koplingslag</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="219"/>
        <source>Output layer</source>
        <translation>Resultatlag</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="268"/>
        <source>Indicates the progress of the join operation</source>
        <translation>Indikerer framdrifta i arbeidet</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="284"/>
        <source>OK to run the join&lt;br&gt;Close to quit&lt;br&gt;Cancel to abort the join</source>
        <translation>Køyr: Utfør koplinga&lt;br&gt;Avslutt: Avslutt programmet&lt;br&gt;Avbryt: Avbryt programmet</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="64"/>
        <source>The base layer for the join.&lt;br&gt;Each feature of this layer will be joined to the nearest neighbour from the join layer.</source>
        <translation>Basislaget for koplinga.&lt;br&gt;Kvart objekt i dette laget vil bli kopla til det næraste objektet i koplingslaget</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="131"/>
        <source>The join layer.&lt;br&gt;A feature from this layer is joined to all the features from the the input layer that has this features as it&apos;s nearest neighbour.</source>
        <translation>Koplingslaget.&lt;br&gt;Eit objekt fra dette laget koplast til alle dei objekta i innlaget som det er næraste nabo til</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="231"/>
        <source>The result layer that contains the join.&lt;br&gt;For each feature of the input layer, the output layer contains that feature with all it&apos;s attributes and all the attributes of the nearest feature in the join layer added.</source>
        <translation>Resultatlaget som inneholder koplinga.&lt;br&gt;For kvart objekt i innlaget vil utlaget inneholde objektet med sine attributt pluss attributtane til det nærastliggande objektet i koplingslaget</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="98"/>
        <source>Use approximate input geometries.&lt;br&gt;This will enable the use of a spatial index - could speed up the join considerably.</source>
        <translation>Bruk forenkla geometriar for innlaget.&lt;br&gt;Dette mogeleggjer bruk av ein romlig indeks, noko som vanlegvis får koplinga til å gå fortare.</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="195"/>
        <source>Join prefix:</source>
        <translation>Prefiks:</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="205"/>
        <source>join_</source>
        <translation>join_</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="143"/>
        <source>Geometry type:</source>
        <translation>Geometritype:</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="156"/>
        <source>Unknown</source>
        <translation>Ukjent</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="167"/>
        <source>Uses an approximation of the geometry (bounding box) for the join</source>
        <translation>Nyttar ei tilnærming til geometrien (omsluttande rektangel) for koplinga.</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="101"/>
        <source>Approximate geometries by centroids</source>
        <translation>Tilnærming (sentroider)</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="170"/>
        <source>Approximate by index geometries</source>
        <translation>Tilnærming</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="202"/>
        <source>The prefix used for the join layer attributes in the result layer.&lt;br&gt;Without a prefix, a join layer attribute that has the same name as an input layer attribute will not be included in the result layer.</source>
        <translation>Prefikset som nyttast for attributtane frå koplingslaget i resultatlaget.&lt;br&gt;Utan prefiks vil ein miste alle attributtar frå koplingslaget som har same navn som ein attributt i inputlaget.</translation>
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
