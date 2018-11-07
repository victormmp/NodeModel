import geojson as gj

def writeGeoJSON(coordinates, outFile):
    
    points = [gj.Point(lon, lat) for lat, lon in coordinates]

    featureCollection = gj.FeatureCollection([gj.Feature(geometry=point) for point in points])

    with open(outFile, 'w') as file:
        gj.dump(featureCollection, file)