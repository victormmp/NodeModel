import geojson as gj

def writeGeoJSON(coordinates, outFile):
    
    points = [gj.Point((coordinate[1], coordinate[0])) for coordinate in coordinates]
    featureCollection = gj.FeatureCollection([gj.Feature(geometry=point) for point in points])

    with open(outFile, 'w') as file:
        gj.dump(featureCollection, file)