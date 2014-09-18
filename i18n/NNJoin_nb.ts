<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS><TS version="2.0">
<context>
    <name>NNJoin</name>
    <message>
        <location filename="NNJoin_plugin.py" line="68"/>
        <source>&amp;NNJoin</source>
        <translation type="unfinished">&amp;NN-kopling</translation>
    </message>
    <message>
        <location filename="NNJoin_plugin.py" line="67"/>
        <source>NNJoin</source>
        <translation type="unfinished">NN-kopling</translation>
    </message>
</context>
<context>
    <name>NNJoinDialog</name>
    <message>
        <location filename="NNJoin_gui.py" line="83"/>
        <source>NNJoin</source>
        <translation type="unfinished">NN-kopling</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="91"/>
        <source>No input layer defined</source>
        <translation type="unfinished">Innlaget mangler</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="97"/>
        <source>No join layer defined</source>
        <translation type="unfinished">Koplingslaget mangler</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="104"/>
        <source>Joining</source>
        <translation type="unfinished">Kopler</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="45"/>
        <source>Cancel</source>
        <translation type="unfinished">Avbryt</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="153"/>
        <source>NNJoin finished</source>
        <translation type="unfinished">NN-kopling avsluttet</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="217"/>
        <source>Killing worker</source>
        <translation type="unfinished">Dreper arbeidsprosessen</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="223"/>
        <source>Error</source>
        <translation type="unfinished">Feil</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="231"/>
        <source>Warning</source>
        <translation type="unfinished">Advarsel</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="239"/>
        <source>Info</source>
        <translation type="unfinished">Informasjon</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="47"/>
        <source>OK</source>
        <translation type="unfinished">Kjør</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="46"/>
        <source>Close</source>
        <translation type="unfinished">Avslutt</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="171"/>
        <source>Worker failed - exception</source>
        <translation type="unfinished">Arbeidsprosessen feilet - avbrudd</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="177"/>
        <source>Worker</source>
        <translation type="unfinished">Arbeidsprosessen</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="161"/>
        <source>Aborted</source>
        <translation type="unfinished">Avbrutt</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="163"/>
        <source>No layer created</source>
        <translation type="unfinished">Ikke noe lag</translation>
    </message>
</context>
<context>
    <name>NNJoinDialogBase</name>
    <message>
        <location filename="ui_frmNNJoin.ui" line="14"/>
        <source>NNJoin</source>
        <translation type="unfinished">NN-kopling</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="41"/>
        <source>Input vector layer</source>
        <translation type="unfinished">Innlag</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="75"/>
        <source>Join vector layer</source>
        <translation type="unfinished">Koplingslag</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="91"/>
        <source>Output layer</source>
        <translation type="unfinished">Resultatlag</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="118"/>
        <source>Indicates the progress of the join operation</source>
        <translation type="unfinished">Indikerer framdrifta i arbeidet</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="134"/>
        <source>OK to run the join&lt;br&gt;Close to quit&lt;br&gt;Cancel to abort the join</source>
        <translation type="unfinished">Kjør: Utfør koplinga&lt;br&gt;Avslutt: Avslutt programmet&lt;br&gt;Avbryt: Avbryt programmet</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="53"/>
        <source>The base layer for the join.&lt;br&gt;Each feature of this layer will be joined to the nearest neighbour from the join layer.</source>
        <translation type="unfinished">Basislaget for koplinga.&lt;br&gt;Hvert objekt i dette laget vil bli kopla til det nærmeste objektet i koplingslaget</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="81"/>
        <source>The join layer.&lt;br&gt;A feature from this layer is joined to all the features from the the input layer that has this features as it&apos;s nearest neighbour.</source>
        <translation type="unfinished">Koplingslaget.&lt;br&gt;Et objekt fra dette laget koples til alle de objektene i innlaget som det er nærmeste nabo til</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="97"/>
        <source>The result layer that contains the join.&lt;br&gt;For each feature of the input layer, the output layer contains that feature with all it&apos;s attributes and all the attributes of the nearest feature in the join layer added.</source>
        <translation type="unfinished">Resultatlaget som inneholder koplinga.&lt;br&gt;For hvert objekt i innlaget vil utlaget inneholde objektet med dets attributter pluss attributtene til det nærmestliggende objektet i koplingslaget</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="60"/>
        <source>Use approximate input geometries.&lt;br&gt;This will enable the use of a spatial index - could speed up the join considerably.</source>
        <translation type="unfinished">Benytt forenklede geometrier for basislaget.&lt;br&gt;Dette muliggjør bruk av en romlig indeks, noe som vanligvis får koplinga til å gå fortere.</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="63"/>
        <source>Approximate geometries using centroids</source>
        <translation type="unfinished">Tilnærmede geometrier (sentroider)</translation>
    </message>
</context>
</TS>
