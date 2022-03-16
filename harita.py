import folium,shutil
import pandas as pd
from folium.plugins import MeasureControl

def create_map(todos):

    try:
        lati_list = []
        longi_list = []
        title_list = []
        height_list = []
        type_list = []
        for i in todos:
            lati_list.append(i.lati)
            longi_list.append(i.longi)
            title_list.append(i.title)
            height_list.append(i.height)
            type_list.append(i.type)
            print("LATi:",i.lati,"Longi:",i.longi)





        int_lat = [float(i) for i in lati_list]
        int_long = [float(i) for i in longi_list]

        # Make a data frame with dots to show on the map
        data = pd.DataFrame({
            'lat': int_long,
            'lon': int_lat,
            'title': title_list,
            'height': height_list,
            'type': type_list,
        })
        data

        # Make an empty map
        m = folium.Map(
            location=[data.iloc[0]['lon'], data.iloc[0]['lat']],
            control_scale=True,
            zoom_start=5
        )
        m.add_child(folium.LatLngPopup())

        for i in range(len(data)):
            html = """
                                    <h1 style="color:green;"> %s</h1><br>
                                    <p>
                                    <code>
                                        Lat: %s<br>
                                        Long: %s<br>
                                    </code>
                                    Height : %s .m<br>
                                    Entered by: %s
                                    </p>
                                    """ % ((data.iloc[i]['type']),(data.iloc[i]['lon']),(data.iloc[i]['lat']),(data.iloc[i]['height']), (data.iloc[i]['title']))

            folium.Marker([data.iloc[i]['lon'], data.iloc[i]['lat']],
                          popup=html,
                          tooltip="Get İnfo"
                          ).add_to(m)

        folium.raster_layers.TileLayer(  # Farklı tür harita desenleri
            tiles='http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr='google',
            name='google maps',
            max_zoom=20,
            subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
            overlay=False,
            control=True,
        ).add_to(m)
        folium.raster_layers.TileLayer(
            tiles='http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            attr='google',
            name='google street view',
            max_zoom=20,
            subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
            overlay=False,
            control=True,
        ).add_to(m)
        folium.LayerControl().add_to(m)
        m.add_child(MeasureControl())  # Mesafe ve Alan ölçer

        # Save it as html
        m.save('/home/atageomatic/nice2/templates/mapper.html')
        #newPath = shutil.copy('mapper.html', '/home/atageomatic/nice2/templates/mapper54.html')

    except IndexError:
        pass