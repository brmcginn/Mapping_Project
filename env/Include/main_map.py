import folium
import pandas

#Creating the Map object
map = folium.Map(location=[40, -99], zoom_start=6, tiles="Stamen Terrain")

#Creating children (a feature group)
fgv = folium.FeatureGroup(name="Volcano Map", )
fgp = folium.FeatureGroup(name="Population Map", )

# Using pandas to read the .txt file
data_frame = pandas.read_csv("env/Include/Volcanoes.txt")

lat = list(data_frame['LAT'])
long = list(data_frame['LON'])
names = list(data_frame['NAME'])
elevations = list(data_frame['ELEV'])

#this is how you originally did it
#for value in lat:
#    index = lat.index(value)
#    latlong_list.append([lat[index], long[index]])
#print(lat[5])
#print(long[5])
#print(latlong_list)
#better way to do it

html = """<h4>Volcano information:</h4>
Height: %s m
"""

def pick_color(elev):
    color = ''
    if 0 < elev <= 1000:
        color = 'green'
    elif 1001 < elev <= 2000:
        color = 'orange'
    else:
        color = 'red'
    return color

#for lat, long in zip(lat, long):
#    print([lat, long])


#Giving each volcanoe a marker with its name and elevation in HTML
for lt, lng, name, elev in zip(lat, long, names, elevations):
    iframe = folium.IFrame(html=html % str(elev), width=200, height=100)
    fgv.add_child(folium.Marker(location=[lt, lng], popup=folium.Popup(iframe), radius = 8, fill_opacity = 0.5,
    icon=folium.Icon(color=pick_color(elev))))

#Adding the polygon layer that allows for population of each country
fgp.add_child(folium.GeoJson(data=open('env/Include/world.json', 'r', encoding='utf-8-sig').read(), 
style_function = lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000001 <= x ['properties']['POP2005']
< 20000000 else 'red' }))

#Adding the feature group to the map
map.add_child(fgp)
map.add_child(fgv)

#adding layer control
map.add_child(folium.LayerControl())

#Final save to update the map HTML object
map.save("env/Include/Map1.html")
