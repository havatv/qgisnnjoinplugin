<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS><TS version="2.0">
<context>
    <name>NNJoin</name>
    <message>
        <location filename="NNJoin_plugin.py" line="80"/>
        <source>&amp;NNJoin</source>
        <translation>&amp;NN-kopling</translation>
    </message>
    <message>
        <location filename="NNJoin_plugin.py" line="79"/>
        <source>NNJoin</source>
        <translation>NN-kopling</translation>
    </message>
    <message>
        <location filename="NNJoin_plugin.py" line="154"/>
        <source>Information</source>
        <translation>Informasjon</translation>
    </message>
    <message>
        <location filename="NNJoin_plugin.py" line="154"/>
        <source>Vector layers not found</source>
        <translation>Ingen vektorlag</translation>
    </message>
</context>
<context>
    <name>NNJoinDialog</name>
    <message>
        <location filename="NNJoin_gui.py" line="53"/>
        <source>NNJoin</source>
        <translation>NN-kopling</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="126"/>
        <source>No input layer defined</source>
        <translation>Innlaget mangler</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="132"/>
        <source>No join layer defined</source>
        <translation>Koplingslaget mangler</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="154"/>
        <source>Joining</source>
        <translation>Kopler</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="54"/>
        <source>Cancel</source>
        <translation>Avbryt</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="211"/>
        <source>NNJoin finished</source>
        <translation>NN-kopling avslutta</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="577"/>
        <source>Error</source>
        <translation>Feil</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="585"/>
        <source>Warning</source>
        <translation>Advarsel</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="593"/>
        <source>Info</source>
        <translation>Informasjon</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="57"/>
        <source>OK</source>
        <translation>Køyr</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="55"/>
        <source>Close</source>
        <translation>Avslutt</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="236"/>
        <source>Worker</source>
        <translation>Arbeidsprosess</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="221"/>
        <source>Aborted</source>
        <translation>Avbrote</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="223"/>
        <source>No layer created</source>
        <translation>Ikkje noko lag</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="56"/>
        <source>Help</source>
        <translation>Hjelp</translation>
    </message>
    <message>
        <location filename="NNJoin_gui.py" line="365"/>
        <source>Information</source>
        <translation>Informasjon</translation>
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
        <location filename="ui_frmNNJoin.ui" line="32"/>
        <source>Input vector layer</source>
        <translation>Innlag</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="130"/>
        <source>Join vector layer</source>
        <translation>Koplingslag</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="278"/>
        <source>Output layer</source>
        <translation>Resultatlag</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="361"/>
        <source>Indicates the progress of the join operation</source>
        <translation>Indikerer framdrifta i arbeidet</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="377"/>
        <source>OK to run the join&lt;br&gt;Close to quit&lt;br&gt;Cancel to abort the join</source>
        <translation>Køyr: Utfør koplinga&lt;br&gt;Avslutt: Avslutt programmet&lt;br&gt;Avbryt: Avbryt programmet</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="52"/>
        <source>The base layer for the join.&lt;br&gt;Each feature of this layer will be joined to the nearest neighbour from the join layer.</source>
        <translation>Basislaget for koplinga.&lt;br&gt;Kvart objekt i dette laget vil bli kopla til det næraste objektet i koplingslaget</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="150"/>
        <source>The join layer.&lt;br&gt;A feature from this layer is joined to all the features from the the input layer that has this features as it&apos;s nearest neighbour.</source>
        <translation>Koplingslaget.&lt;br&gt;Eit objekt fra dette laget koplast til alle dei objekta i innlaget som det er næraste nabo til</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="290"/>
        <source>The result layer that contains the join.&lt;br&gt;For each feature of the input layer, the output layer contains that feature with all it&apos;s attributes and all the attributes of the nearest feature in the join layer added.</source>
        <translation>Resultatlaget som inneholder koplinga.&lt;br&gt;For kvart objekt i innlaget vil utlaget inneholde objektet med sine attributt pluss attributtane til det nærastliggande objektet i koplingslaget</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="256"/>
        <source>Join prefix:</source>
        <translation>Prefiks:</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="266"/>
        <source>join_</source>
        <translation>join_</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="157"/>
        <source>Geometry type:</source>
        <translation>Geometritype:</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="169"/>
        <source>Unknown</source>
        <translation>Ukjent</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="105"/>
        <source>Approximate geometries by centroids</source>
        <translation>Tilnærming (sentroider)</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="263"/>
        <source>The prefix used for the join layer attributes in the result layer.&lt;br&gt;Without a prefix, a join layer attribute that has the same name as an input layer attribute will not be included in the result layer.</source>
        <translation>Prefikset som nyttast for attributtane frå koplingslaget i resultatlaget.&lt;br&gt;Utan prefiks vil ein miste alle attributtar frå koplingslaget som har same navn som ein attributt i inputlaget.</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="203"/>
        <source>Approximate geometries</source>
        <translation>Omtrentlege geometriar</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="210"/>
        <source>Use an index to speed up the join</source>
        <translation>Bruk ein romleg indeks for å få koplinga til å gå fortare</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="213"/>
        <source>Use index</source>
        <translation>Bruk indeks</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="102"/>
        <source>Use approximate input geometries.&lt;br&gt;The result will also be approximate.&lt;br&gt;Could speed up the join considerably.</source>
        <translation>Bruk tilnærma inngeometriar.&lt;br&gt;Resultatet vil også være tilnærma.&lt;br&gt;Kan få koplinga til å gå fortare.</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="200"/>
        <source>Uses an approximation of the geometry (bounding box) for the join.&lt;br/&gt;The result will also be approximate.</source>
        <translation>Bruk tilnærma koplingsgeometri.&lt;br&gt;Resultatet vil også være tilnærma.</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="393"/>
        <source>Get some help</source>
        <translation>Få hjelp</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="396"/>
        <source>Help</source>
        <translation>Hjelp</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="315"/>
        <source>Neighbour distance field:</source>
        <translation>Felt for naboavstand</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="322"/>
        <source>The field name used for the distance to the nearest neighbour.&lt;br&gt;Can not be the same as an existing field name.</source>
        <translation>Namnet til feltet med avstand til nærmaste nabo.&lt;br&gt;Kan ikkje vere likt eit eksisterande feltnamn.</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="325"/>
        <source>distance</source>
        <translation>avstand</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="189"/>
        <source>Selected only</source>
        <translation>Kun valgte</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="239"/>
        <source>Avoids joining geometries that have a contained relation</source>
        <translation>Unngår å kople geometriar som har eit "inneholdt i"-forhold</translation>
    </message>
    <message>
        <location filename="ui_frmNNJoin.ui" line="242"/>
        <source>Exclude containing</source>
        <translation>Ekskluder "inneholdt i"</translation>
    </message>
</context>
<context>
    <name>Worker</name>
    <message>
        <location filename="NNJoin_engine.py" line="424"/>
        <source>CRS Transformation error!</source>
        <translation>Koordinattransformasjonsfeil!</translation>
    </message>
</context>
</TS>
