// render json sample information on the openlayers map

var Sample = {
        initStyles: function() {
            if (_.isUndefined(this.styles)){
                this.styles = {};
                this.styles['iconStyle'] = new ol.style.Style({
                    image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
                        src: '/static/xgds_sample/images/sample_icon.png',
                        scale: 0.8
                        }))
                      });
                this.styles['text'] = {
                    font: '12px Calibri,sans-serif',
                    fill: new ol.style.Fill({
                        color: 'black'
                    }),
                    stroke: new ol.style.Stroke({
                        color: 'yellow',
                        width: 2
                    }),
                    offsetY: -15
                };
            }
        },
        constructElements: function(samplesJson){
            if (_.isEmpty(samplesJson)){
                return null;
            }
            this.initStyles();
            var olFeatures = [];
            for (var i = 0; i < samplesJson.length; i++) {
                if (samplesJson[i].lat !== "") {
                    var sampleFeature = this.constructMapElement(samplesJson[i]);
                    olFeatures = olFeatures.concat(sampleFeature);
                }
            }
            var vectorLayer = new ol.layer.Vector({
                name: "Samples",
                source: new ol.source.Vector({
                    features: olFeatures
                }),
            });  
            return vectorLayer;
        },
        constructMapElement:function(sampleJson){
            var coords = transform([sampleJson.lon, sampleJson.lat]);
            var feature = new ol.Feature({
                name: sampleJson.name,
                geometry: new ol.geom.Point(coords)
            });
            feature.setStyle(this.getStyles(sampleJson));
            this.setupPopup(feature, sampleJson);
            return feature;
        },
        getStyles: function(sampleJson) {
            var styles = [this.styles['iconStyle']];
            var theText = new ol.style.Text(this.styles['text']);
            theText.setText(sampleJson.name);
            var textStyle = new ol.style.Style({
                text: theText
            });
            styles.push(textStyle);
            return styles;
        },
        setupPopup: function(feature, sampleJson) {
            var trString = "<tr><td>%s</td><td>%s</td></tr>";
            var formattedString = "<table>";
            for (j = 0; j< 7; j++){
                formattedString = formattedString + trString;
            }
            formattedString = formattedString + "</table>";
            var data = ["Label:", sampleJson.label_number,
                        "Name:", sampleJson.name ? sampleJson.name : '',
                        "Type:", sampleJson.sample_type_name,
                        "Region:", sampleJson.region_name,
                        "Collector:", sampleJson.collector_name ? sampleJson.collector_name: '',
                        "Time:", sampleJson.collection_time ? getLocalTimeString(sampleJson.collection_time, sampleJson.collection_timezone):'',
                        "Description:", sampleJson.description ? sampleJson.description : ''];
            var popupContents = vsprintf(formattedString, data);
            feature['popup'] = popupContents;
        }
}